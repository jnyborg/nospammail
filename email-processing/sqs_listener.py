import boto3
import json
import os
import sys
import threading
from multiprocessing.dummy import Pool as ThreadPool

from email_processor import processEmail

def ListenForMails():
    THREAD_COUNT = max(os.cpu_count() - 1, 4)  # Leave dedicated thread for listener, minimum of 4 threads though

    try:
        threadArg = int(sys.argv[1]) # First argument overrides thread pool size

        if threadArg > 0:
            THREAD_COUNT = threadArg
    except IndexError: # No thread count was specified
        pass

    pool = ThreadPool(THREAD_COUNT)

    client = boto3.setup_default_session(region_name='eu-west-1')

    sqs = boto3.resource('sqs')

    queue = sqs.get_queue_by_name(QueueName='NoSpamMailQueue')

    print("Listening to queue %s" % queue.url)
    print("Current delay is %s" % queue.attributes.get('DelaySeconds'))

    while True:
        pool.map(ReceiveEmail, queue.receive_messages(MessageAttributeNames=['Author']))

    pool.close()
    pool.join()

def ReceiveEmail(message):
    print("There's a new message! Thread {} is handling it.".format(threading.get_ident()))

    processEmail(json.loads(message.body))

    message.delete()

if __name__ == "__main__":
    ListenForMails()
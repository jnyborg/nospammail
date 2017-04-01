import boto3
import json

client = boto3.setup_default_session(region_name='eu-west-1')

sqs = boto3.resource('sqs')

queue = sqs.get_queue_by_name(QueueName='NoSpamMailQueue')

print("Listening to queue %s" % queue.url)
print("Current delay is %s" % queue.attributes.get('DelaySeconds'))

while True:
    for message in queue.receive_messages(MessageAttributeNames=['Author']):
        print("There's a new message!")
        author_text = ""
        if message.message_attributes is not None:
            author_name = message.message_attributes.get('Author').get('StringValue')
            if author_name:
                author_text = " ({0})".format(author_name)

        #print("Full message: {0}!{1}".format(message.body, author_text))
        messageJson = json.loads(message.body)
        print("Subject: %s" % messageJson['Subject'])
        print("Message: %s" % messageJson['Message'])

        message.delete()
        #break Used for the else statement
    #else:
        #print("Queue is empty!")
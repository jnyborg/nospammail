import json
import smtplib

def processEmail(message):
    #print("message: %s" % message)
    d = json.loads(message['Message'])
    #print("d: %s" % d)
    m = d['mail']
    #print("m: %s" % m)
    source = m['source']
    print("source: %s" % source)
    destinations = m['destination']
    destinationsPrefix = map(lambda x: x.split('@')[0], destinations)
    print("destinations:")
    for des in destinations:
        print(des)

    print("destinationsPre:")
    for des in destinationsPrefix:
        print(des)

    subject = m['commonHeaders']['subject']
    print("subject: %s" % subject)

    actualEmail = "jnyborg@outlook.com"

    sender = destinations[0]
    receivers = [ actualEmail ]
    print(m)
    msg = d['content']

    try:
        smtpObj = smtplib.SMTP('localhost', 25)
        smtpObj.sendmail(sender, receivers, msg)
        print("Successfully sent email!")
    except smtplib.SMTPException as e:
        print("ERROR: %s: %s" % e.errno, e.strerror)

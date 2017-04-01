import json
import smtplib

def processEmail(message):
    print("message: %s" % message)
    print("dumped: %s" % json.dumps(message))
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

    actualEmail = "alexander@svejbaekgaard.dk"

    sender = destinations[0]
    receivers = [ actualEmail ]
    print(m)
    msg = d['content']

    try:
        smtpObj = smtplib.SMTP(host="nospammail.org", port=25, local_hostname="localhost")
        smtpObj.sendmail(sender, receivers, msg)
        print("Successfully sent email!")
    except smtplib.SMTPException:
        print("ERROR, email not sent!")

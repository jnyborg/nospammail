import json
import smtplib
import psycopg2
import os

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

    try:
        conn = psycopg2.connect("dbname='nospammail' " \
                                "user='nospammail' " \
                                "host='{}'" \
                                "password='{}'".format(
                                        os.environ.get('NOSPAMMAIL_HOST', False),
                                        os.environ.get('NOSPAMMAIL_PW', False)))

        cur = conn.cursor()
        cur.execute("select g.enabled as enabled, u.email as email from settings_console_generatedemail as g left join auth_user as u on g.id = u.user_id where g.email={};".format(destinations[0]))
        rows = cur.fetchall()

        if len(rows) <= 0:
            print("Error, {} has no owner!".format(destinations[0]))
            return
        else:
            if rows[0]['enabled']:
                sender = destinations[0]
                receivers = [rows[0]['email']]
                print(m)
                msg = d['content']

                try:
                    smtpObj = smtplib.SMTP('localhost', 25)
                    smtpObj.sendmail(sender, receivers, msg)
                    print("Successfully sent email!")
                except smtplib.SMTPException as e:
                    print("ERROR: %s: %s" % e.errno, e.strerror)
            else:
                print("Email linked to {} has disabled forwarding.".format(destinations[0]))
    except:
        print("Unable to connect to database!")






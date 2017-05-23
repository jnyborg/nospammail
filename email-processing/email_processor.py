import json
import smtplib
import psycopg2
import os

def processEmail(message):

    d = json.loads(message['Message'])

    m = d['mail']

    sender = m['source']
    destinationsTemp = m['destination']

    destinations = list(filter(lambda x: "@nospammail.org" in x, destinationsTemp)) # Remove any emails that aren't sent to the nospammail.org domain

    forwarder = destinations[0]

    print("Should forward email to:")
    for des in destinations:
        print(des)

    try:
        conn = psycopg2.connect("dbname='nospammail' " \
                                "user='nospammail' " \
                                "host='{}'" \
                                "password='{}'".format(
                                        os.environ.get('NOSPAMMAIL_HOST', False),
                                        os.environ.get('NOSPAMMAIL_PW', False)))
        
        cur = conn.cursor()
        cur.execute("select g.enabled as enabled, u.email as email from settings_console_generatedemail as g left join auth_user as u on g.user_id = u.id where g.email='{}';".format(forwarder))
        rows = cur.fetchall()

        if len(rows) <= 0:
            print("Error, {} has no owner! Sender was {}".format(destinations[0], sender))
            return
        else:
            if rows[0][0]:
                forwarder = destinations[0]
                receivers = [rows[0][1]]
                msg = d['content']

                try:
                    smtpObj = smtplib.SMTP('localhost', 25)
                    smtpObj.sendmail(forwarder, receivers, msg)
                    print("Successfully sent email!")
                except smtplib.SMTPException as e:
                    print("ERROR: %s: %s" % e.errno, e.strerror)
            else:
                print("Email linked to {} has disabled forwarding.".format(destinations[0]))
    except psycopg2.Error as e:
        if hasattr(e, 'reason') and hasattr(e, 'code'):
            print("Unable to connect to DB, error code: {}, error reason: {}".format(e.code, e.reason))
        elif hasattr(e, 'reason'):
            print("Unable to connect to DB, error reason: {}".format(e.reason))
        elif hasattr(e, 'code'):  # <--
            print("Unable to connect to DB, error code: {}".format(e.code))
        elif hasattr(e, 'errno'):
            print("Unable to connect to DB: {}: {}".format(e.errno, e.strerror))
        else:
            print("Unable to connect to DB: unspecified error: {}".format(str(e)))
    except Exception as e:
        if hasattr(e, 'reason'):
            print("Undefined exception, error reason: {}".format(e.reason))
        elif hasattr(e, 'code'):  # <--
            print("Undefined exception, error code: {}".format(e.code))
        elif hasattr(e, 'errno'):
            print("Undefined exception: {}: {}".format(e.errno, e.strerror))
        else:
            print("UUndefined exception: unspecified error: {}".format(str(e)))
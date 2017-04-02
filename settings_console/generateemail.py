import string
import random
import psycopg2
import os

def __generatePrefix():
    allowedCharacters = string.ascii_lowercase + "".join(map(str, range(10)))

    tempEmail = ""
    for num in range(10):
        tempEmail += allowedCharacters[random.randint(0, len(allowedCharacters) - 1)]

    return tempEmail

def __emailIsUnique(email):
    try:
        conn = psycopg2.connect("dbname='nospammail' " \
                                "user='nospammail' " \
                                "host='{}'" \
                                "password='{}'".format(
                                        os.environ.get('NOSPAMMAIL_HOST', False),
                                        os.environ.get('NOSPAMMAIL_PW', False)))

        cur = conn.cursor()
        cur.execute("select * from settings_console_generatedemail as g where g.email='{}';".format(email))
        rows = cur.fetchall()

        return len(rows <= 0)
    except Exception as e:
        print("Unable to connect to DB: %s: %s" % e.errno, e.strerror)

    return False

def generateRandomEmail():
    emailSuffix = "@nospamemail.org"

    newEmail = __generatePrefix()

    while not __emailIsUnique(newEmail):
        print("Email {} was not uinque!".format(newEmail))
        newEmail = __generatePrefix()

    return newEmail + emailSuffix

if __name__ == "__main__":
    print(generateRandomEmail())
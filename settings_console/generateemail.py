import string
import random

def __generatePrefix():
    allowedCharacters = string.ascii_lowercase + "".join(map(str, range(10)))

    tempEmail = ""
    for num in range(10):
        tempEmail += allowedCharacters[random.randint(0, len(allowedCharacters) - 1)]

    return tempEmail

def __emailIsUnique(email):
    takenEmails = []
    for n in range(30):
        takenEmails.insert(n, __generatePrefix())

    #print(email + " taken: " + str(email in takenEmails))
    return not email in takenEmails

def generateRandomEmail():
    emailSuffix = "@nospamemail.org"

    newEmail = __generatePrefix()

    while not __emailIsUnique(newEmail):
        newEmail = __generatePrefix()

    return newEmail + emailSuffix

if __name__ == "__main__":
    print(generateRandomEmail())
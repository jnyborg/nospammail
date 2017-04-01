import string
import random

def __generatePrefix():
    allowedCharacters = string.ascii_lowercase + "".join(map(str, range(10)))

    tempEmail = ""
    for num in range(10):
        tempEmail += allowedCharacters[random.randint(0, len(allowedCharacters) - 1)]

    return tempEmail

def generateRandomEmail():
    emailSuffix = "@nospamemail.org"

    takenEmails = []
    for n in range(30):
        takenEmails.insert(n, __generatePrefix())

    newEmail = __generatePrefix()

    while(newEmail in takenEmails):
        #print(newEmail + " taken: " + str(newEmail in takenEmails))
        newEmail = __generatePrefix()

    #print(newEmail + " taken: " + str(newEmail in takenEmails))
    return newEmail + emailSuffix

if __name__ == "__main__":
    print(generateRandomEmail())
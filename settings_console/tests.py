from django.test import TestCase
from django.contrib import auth
from django.contrib.auth.models import User
from settings_console.models import GeneratedEmail

validUsername = "testuser"
validEmail = "testuser@gmail.com"
validPassword = "secretpass333"
validEmailDescription = "This is a valid description"


def registerAndLogin(self, username=None, password=None, email=None):
    if username == None or password == None or email == None:
        _username = validUsername
        _password = validPassword
        _email = validEmail
    else:
        _username = username
        _password = password
        _email = email

    User.objects.create_user(_username, _email, _password)
    logIn(self, _username, _password)

def logIn(self, username, password):

    params = {'username': username, 'password': password}
    self.client.post("/login/", data=params)

def logOut(self):

    self.client.post("/logout/")

class TestEmailGeneration(TestCase):

    def test_shouldBeAbleToGenerateEmailWhileLoggedIn(self):
        """
        Users should be able to generate a new email once logged in 
        """

        registerAndLogin(self)

        self.client.get("/ajax/add_email/", data={ 'description': validEmailDescription })

        emails = GeneratedEmail.objects.all()

        self.assertTrue(len(emails) == 1, "Failed to generate email")

    def test_generatedEmailShouldBeAssignedCorrectUserId(self):
        """
        Emails generated should be assigned the correct user id
        """

        registerAndLogin(self)

        self.client.get("/ajax/add_email/", data={ 'description': validEmailDescription + "1" })

        user = auth.get_user(self.client)
        emails = GeneratedEmail.objects.filter(user_id=user.id)

        self.assertTrue(len(emails) == 1, "User id was not correct")
    
    def test_shouldNotBeAbleToGenerateEmailWhileNotLoggedIn(self):
        """
        Users should not be able to generate a new email while not logged in
        """

        self.client.get("/ajax/add_email/", data={ 'description': validEmailDescription })

        emails = GeneratedEmail.objects.all()
        self.assertTrue(len(emails) == 0, "Generated email for unauthorized user")

    def test_shouldBeAbleToGenerateEmailMultipleEmails(self):
        """
        Users should be able to generate multiple emails
        """

        registerAndLogin(self)

        emailsToGenerate = 5

        for i in range(emailsToGenerate):
            self.client.get("/ajax/add_email/", data={ 'description': validEmailDescription + str(i) })

        emails = GeneratedEmail.objects.all()
        self.assertTrue(len(emails) == emailsToGenerate, "Failed to generate multiple emails")

    def test_shouldBeAbleToGenerateEmailMultipleEmailsWithSameDescription(self):
        """
        Users should be able to generate multiple emails with the same description
        """

        registerAndLogin(self)

        for i in range(2):
            self.client.get("/ajax/add_email/", data={ 'description': validEmailDescription })

        emails = GeneratedEmail.objects.all()

        self.assertTrue(len(emails) == 2, "Failed to generate multiple emails with same description")
        self.assertTrue(emails[0].description == emails[1].description, "Emails created with same description had did not have the same description")

    def test_shouldBeAbleToEnableEmail(self):
        """
        Users should be able to enable forwarding of emails
        """

        registerAndLogin(self)

        self.client.get("/ajax/add_email/", data={ 'description': validEmailDescription })

        email = GeneratedEmail.objects.all()[0]

        initialState = email.enabled
        self.client.get("/ajax/toggle_email/", data={ 'id': email.id})

        newState = GeneratedEmail.objects.all()[0].enabled

        self.assertNotEqual(initialState, newState, "Failed to enable email forwarding")

    def test_shouldBeAbleToDisableEmail(self):
        """
        Users should be able to disable forwarding of emails
        """

        registerAndLogin(self)

        self.client.get("/ajax/add_email/", data={ 'description': validEmailDescription })

        email = GeneratedEmail.objects.all()[0]

        initialState = email.enabled
        self.client.get("/ajax/toggle_email/", data={ 'id': email.id})
        self.client.get("/ajax/toggle_email/", data={ 'id': email.id})

        newState = GeneratedEmail.objects.all()[0].enabled

        self.assertEqual(initialState, newState, "Failed to enable email forwarding")

    def test_shouldNotBeAbleToToggleOthersEmails(self):
        """
        Users should not be able to toggle emails that are not theirs
        """

        registerAndLogin(self)

        self.client.get("/ajax/add_email/", data={ 'description': validEmailDescription })

        logOut(self)

        registerAndLogin(self, validUsername + "1", validPassword + "1", "1" + validEmail)

        self.client.get("/ajax/add_email/", data={ 'description': validEmailDescription })

        email = GeneratedEmail.objects.all().order_by("-id")[1] # Emails ordered by id ascending

        initialState = email.enabled
        self.client.get("/ajax/toggle_email/", data={ 'id': email.id})

        newState = GeneratedEmail.objects.all()[0].enabled

        self.assertEqual(initialState, newState, "Illegally changed another users forwarding setting")

    def test_shouldNotBeAbleToToggleEmailsAfterLoggingOut(self):
        """
        Users should not be able to toggle emails after logging out
        """

        registerAndLogin(self)

        self.client.get("/ajax/add_email/", data={ 'description': validEmailDescription })

        logOut(self)

        email = GeneratedEmail.objects.all()[0]

        initialState = email.enabled
        self.client.get("/ajax/toggle_email/", data={ 'id': email.id})

        newState = GeneratedEmail.objects.all()[0].enabled

        self.assertEqual(initialState, newState, "Illegally changed forwarding setting after logging out")
from django.test import TestCase
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from settings_console.models import GeneratedEmail
from http import HTTPStatus

validUsername = "testuser"
validEmail = "testuser@gmail.com"
validPassword = "secretpass333"
validEmailDescription = "This is a valid description"
validUsername2 = "testuser2"
validEmail2 = "testuser2@gmail.com"
validPassword2 = "secretpass444"
validEmailDescription2 = "This is a valid description2"

def registerAndLogin(self, username=None, password=None, email=None):
    if username == None or password == None or email == None:
        _username = validUsername
        _password = validPassword
        _email = validEmail
    else:
        _username = username
        _password = password
        _email = email


    self.client.post(reverse('signup'), { 'username': _username, 'email': _email, 'password1': _password, 'password2': _password})

    return logIn(self, _username, _password)

def logIn(self, username, password):

    params = {'username': username, 'password': password}
    return self.client.post(reverse('login'), data=params)

def logOut(self):

    return self.client.post("/logout/")

def addEmail(self, description):

    return self.client.get("/ajax/add_email/", data={'description': description})

def toggleEmail(self, id):

    return self.client.get("/ajax/toggle_email/", data={'id': id})

class TestEmailGeneration(TestCase):

    def test_shouldBeAbleToGenerateEmailWhileLoggedIn(self):
        """
        Users should be able to generate a new email once logged in 
        """

        registerAndLogin(self)

        addEmail(self, validEmailDescription)

        emails = GeneratedEmail.objects.all()

        self.assertTrue(len(emails) == 1, "Failed to generate email")

    def test_generatedEmailShouldBeAssignedCorrectUserId(self):
        """
        Emails generated should be assigned the correct user id
        """

        registerAndLogin(self)

        addEmail(self, validEmailDescription)

        user = auth.get_user(self.client)
        emails = GeneratedEmail.objects.filter(user_id=user.id)

        self.assertTrue(len(emails) == 1, "User id was not correct")
    
    def test_shouldNotBeAbleToGenerateEmailWhileNotLoggedIn(self):
        """
        Users should not be able to generate a new email while not logged in
        """

        addEmail(self, validEmailDescription)

        emails = GeneratedEmail.objects.all()
        self.assertTrue(len(emails) == 0, "Generated email for unauthorized user")

    def test_shouldBeAbleToGenerateEmailMultipleEmails(self):
        """
        Users should be able to generate multiple emails
        """

        registerAndLogin(self)

        emailsToGenerate = 5

        for i in range(emailsToGenerate):
            addEmail(self, validEmailDescription + str(i))

        emails = GeneratedEmail.objects.all()
        self.assertTrue(len(emails) == emailsToGenerate, "Failed to generate multiple emails")

    def test_shouldBeAbleToGenerateEmailMultipleEmailsWithSameDescription(self):
        """
        Users should be able to generate multiple emails with the same description
        """

        registerAndLogin(self)

        for i in range(2):
            addEmail(self, validEmailDescription)

        emails = GeneratedEmail.objects.all()

        self.assertTrue(len(emails) == 2, "Failed to generate multiple emails with same description")
        self.assertTrue(emails[0].description == emails[1].description, "Emails created with same description had did not have the same description")

    def test_shouldBeAbleToEnableEmail(self):
        """
        Users should be able to enable forwarding of emails
        """

        registerAndLogin(self)

        addEmail(self, validEmailDescription)

        email = GeneratedEmail.objects.all()[0]

        initialState = email.enabled
        toggleEmail(self, email.id)

        newState = GeneratedEmail.objects.all()[0].enabled

        self.assertNotEqual(initialState, newState, "Failed to enable email forwarding")

    def test_shouldBeAbleToDisableEmail(self):
        """
        Users should be able to disable forwarding of emails
        """

        registerAndLogin(self)

        addEmail(self, validEmailDescription)

        email = GeneratedEmail.objects.all()[0]

        initialState = email.enabled
        toggleEmail(self, email.id)
        toggleEmail(self, email.id)

        newState = GeneratedEmail.objects.all()[0].enabled

        self.assertEqual(initialState, newState, "Failed to enable email forwarding")

    def test_shouldNotBeAbleToToggleOthersEmails(self):
        """
        Users should not be able to toggle emails that are not theirs
        """

        registerAndLogin(self)

        addEmail(self, validEmailDescription)

        logOut(self)

        registerAndLogin(self, validUsername2, validPassword2, validEmail2)

        addEmail(self, validEmailDescription)

        email = GeneratedEmail.objects.all().order_by("-id")[1] # Emails ordered by id ascending

        initialState = email.enabled
        toggleEmail(self, email.id)

        newState = GeneratedEmail.objects.all()[0].enabled

        self.assertEqual(initialState, newState, "Illegally changed another users forwarding setting")

    def test_shouldNotBeAbleToToggleEmailsAfterLoggingOut(self):
        """
        Users should not be able to toggle emails after logging out
        """

        registerAndLogin(self)

        addEmail(self, validEmailDescription)

        logOut(self)

        email = GeneratedEmail.objects.all()[0]

        initialState = email.enabled
        toggleEmail(self, email.id)

        newState = GeneratedEmail.objects.all()[0].enabled

        self.assertEqual(initialState, newState, "Illegally changed forwarding setting after logging out")

    def test_emailsGeneratedFromDifferentUsersShouldHaveDifferentUserId(self):
        """
        Emails generated from different users should have different user ids
        """

        registerAndLogin(self)

        addEmail(self, validEmailDescription)

        logOut(self)

        registerAndLogin(self, validUsername2, validPassword2, validEmail2)
        addEmail(self, validEmailDescription)

        email1 = GeneratedEmail.objects.all()[0]
        email2 = GeneratedEmail.objects.all()[1]

        self.assertNotEqual(email1.user_id, email2.user_id, "Different users generated emails with same user id")

    def test_shouldNotBeAbleToRegisterWhileLoggedIn(self):
        """
        Users should not be able to register a new account while already logged in
        """

        registerAndLogin(self)

        response = self.client.post(reverse('signup'), { 'username': validUsername2, 'email': validEmail2, 'password1': validPassword2, 'password2': validPassword2})

        self.assertEquals(len(User.objects.all()), 1, "Created account while already logged in")

    def test_registeringWhileLoggedInShouldReturn401Unauthorized(self):
        """
        Users should not be able to register a new account while already logged in, instead they should get a 401 unauthorized
        """

        registerAndLogin(self)

        response = self.client.post(reverse('signup'), { 'username': validUsername2, 'email': validEmail2, 'password1': validPassword2, 'password2': validPassword2})

        self.assertEquals(HTTPStatus(response.status_code), HTTPStatus.UNAUTHORIZED, "Registering a new account while already logged in did not return a status code {}".format(HTTPStatus.UNAUTHORIZED))

    def test_registeringWhileLoggedInShouldRemainLoggedIn(self):
        """
        Users should remain logged in when attempting to register a new account while already logged in
        """

        registerAndLogin(self)

        self.client.post(reverse('signup'), { 'username': validUsername2, 'email': validEmail2, 'password1': validPassword2, 'password2': validPassword2})

        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated(), "Registering a new account while already logged in deleted session")

    def test_registeringWhileLoggedInShouldRemainLoggedInToSameAccount(self):
        """
        Users should remain logged in to the same account when attempting to register a new account while already logged in
        """

        registerAndLogin(self)

        originalUser = auth.get_user(self.client)

        self.client.post(reverse('signup'), { 'username': validUsername2, 'email': validEmail2, 'password1': validPassword2, 'password2': validPassword2})

        newUser = auth.get_user(self.client)

        self.assertEquals(originalUser.id, newUser.id, "Registering a new account while already logged in login session")

    def test_shouldNotBeAbleToLogInWhileLoggedIn(self):
        """
        Users should not be able to log in while already logged in
        """

        User.objects.create_user(validUsername2, validEmail2, validPassword2)

        response = registerAndLogin(self)

        oldUser = auth.get_user(self.client)

        logIn(self, validUsername2, validPassword2)

        newUser = auth.get_user(self.client)

        self.assertEquals(oldUser, newUser, "Logged into an account while already logged in")
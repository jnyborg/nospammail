from django.test import TestCase
from login.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

validUsername = "testuser"
validEmail = "testuser@gmail.com"
validPassword = "secretpass333"
validEmailDescription = "This is a valid description"
validUsername2 = "testuser2"
validEmail2 = "testuser2@gmail.com"
validPassword2 = "secretpass444"
validEmailDescription2 = "This is a valid description2"

def registerAndLogin(self, username=None, password=None, password2=None, email=None):
    if username == None or password == None or email == None:
        _username = validUsername
        _password = validPassword
        _password2 = validPassword
        _email = validEmail
    else:
        _username = username
        _password = password
        _password2 = password2 if password2 is not None else password
        _email = email

    self.client.post(reverse('signup'), { 'username': _username, 'email': _email, 'password1': _password, 'password2': _password2})

    return logIn(self, _username, _password)

def logIn(self, username, password):

    params = {'username': username, 'password': password}
    return self.client.post(reverse('login'), data=params)

def logOut(self):

    return self.client.post("/logout/")

class TestInputValidation(TestCase):

    def test_registeredUserCanLogIn(self):
        """
        Users should be able to register and log in 
        """

        registerAndLogin(self, username=validUsername, password=validPassword, email=validEmail)

        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated(), "Registered user could not log in")

    def test_unregisteredUserCannotLogIn(self):
        """
        Users should not be able to log in without registering first 
        """

        params = {'username': validUsername, 'password': validPassword}
        self.client.post("/login/", data=params)
        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated(), "Unregistered user could log in")

    def test_loggingOutShouldDeauthenticate(self):
        registerAndLogin(self, username=validUsername, password=validPassword, email=validEmail)

        logOut(self)

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated(), "User was still logged in after calling log out")

    def test_emailCannotContainNoSpamMail(self):
        """
        clean() should disallow registration using a "@nospammail" email address.
        """
        email = "abcdefg@nospammail.org"

        params = { 'username': validUsername, 'email': email, 'password1': validPassword, 'password2': validPassword}
        form = UserCreationForm(params)

        form.is_valid()

        self.assertRaises(ValidationError, form.clean)

    def test_emailWithoutNoSpamMailIsAllowed(self):
        """
        clean() should allow registration using a "@gmail" email address.
        """

        params = { 'username': validUsername, 'email': validEmail, 'password1': validPassword, 'password2': validPassword}
        form = UserCreationForm(params)

        form.is_valid()

        form.clean()

    def test_emailSqlInjectionShouldRemoveEmail(self):
        """
        is_valid() should prevent sql injection
        """
        email = "test@gmail.com'; DELETE auth_user;"

        params = {'username': validUsername, 'email': email, 'password1': validPassword, 'password2': validPassword}
        form = UserCreationForm(params)

        form.is_valid()

        self.assertNotIn("email", form.cleaned_data, "form.clean did not remove sql injection")

    def test_shouldLogInAfterRegistration(self):
        """
        User should be logged in directly after registration
        """

        registerAndLogin(self, username=validUsername, password=validPassword, email=validEmail)

        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated(), "Did not automatically log in after registering account")

    def test_shouldNotLogInAfterFailedRegistration(self):
        """
        User should not be logged in directly after failed registration
        """

        email = "abcdefg22@nospammail.org"

        registerAndLogin(self, username=validUsername, password=validPassword, email=email)

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated(), "Logged in after failed registration")

    def test_cannotRegisterWithEmptyUsername(self):
        """
        User cannot register with empty username
        """

        registerAndLogin(self, username="", password=validPassword, email=validEmail)

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated(), "Registered with an empty username")

    def test_cannotRegisterWithEmptyEmail(self):
        """
        User cannot register with empty email
        """

        registerAndLogin(self, username=validUsername, password=validPassword, email="")

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated(), "Registered with an empty email")

    def test_cannotRegisterWithEmptyPassword1(self):
        """
        User cannot register with empty password1
        """

        registerAndLogin(self, username=validUsername, password="", email=validEmail)

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated(), "Registered with an empty password1")

    def test_cannotRegisterWithEmptyPassword2(self):
        """
        User cannot register with empty password2
        """

        registerAndLogin(self, username=validUsername, password=validPassword, password2="", email=validEmail)

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated(), "Registered with an empty password2")

    def test_emailShouldBeUnique(self):

        registerAndLogin(self, username=validUsername, password=validPassword, email=validEmail)

        logOut(self)

        registerAndLogin(self, username=validUsername2, password=validPassword2, email=validEmail)

        self.assertEquals(User.objects.count(), 1, "Registered two accounts with same email address")

    def test_usernameShouldBeUnique(self):

        registerAndLogin(self, username=validUsername, password=validPassword, email=validEmail)

        logOut(self)

        registerAndLogin(self, username=validUsername, password=validPassword2, email=validEmail2)

        self.assertEquals(User.objects.count(), 1, "Registered two accounts with same username")

    def test_passwordShouldNotBeUnique(self):

        registerAndLogin(self, username=validUsername, password=validPassword, email=validEmail)

        logOut(self)

        registerAndLogin(self, username=validUsername2, password=validPassword, email=validEmail2)

        self.assertEquals(User.objects.count(), 2, "Could not register two accounts with same password")
from django.test import TestCase
from login.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

validUsername = "testuser"
validEmail = "testuser@gmail.com"
validPassword = "secretpass333"

class TestInputValidation(TestCase):
    
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

        self.assertNotIn("email", form.cleaned_data)

    def test_shouldLogInAfterRegistration(self):
        """
        User should be logged in directly after registration
        """

        self.client.post(reverse('signup'), { 'username': validUsername, 'email': validEmail, 'password1': validPassword, 'password2': validPassword})

        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated())

    def test_shouldNotLogInAfterFailedRegistration(self):
        """
        User should not be logged in directly after failed registration
        """

        email = "abcdefg22@nospammail.org"
        self.client.post(reverse('signup'), { 'username': validUsername, 'email': email, 'password1': validPassword, 'password2': validPassword})

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated())

    def test_cannotRegisterWithEmptyUsername(self):
        """
        User cannot register with empty username
        """

        self.client.post(reverse('signup'), { 'username': "", 'email': validEmail, 'password1': validPassword, 'password2': validPassword})

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated())

    def test_cannotRegisterWithEmptyEmail(self):
        """
        User cannot register with empty email
        """

        self.client.post(reverse('signup'), { 'username': validUsername, 'email': "", 'password1': validPassword, 'password2': validPassword})

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated())

    def test_cannotRegisterWithEmptyPassword1(self):
        """
        User cannot register with empty password1
        """

        self.client.post(reverse('signup'), { 'username': validUsername, 'email': validEmail, 'password1': "", 'password2': validPassword})

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated())

    def test_cannotRegisterWithEmptyPassword2(self):
        """
        User cannot register with empty password2
        """

        self.client.post(reverse('signup'), { 'username': validUsername, 'email': validEmail, 'password1': validPassword, 'password2': ""})

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated())

    def test_registeredUserCanLogIn(self):

        User.objects.create_user(validUsername, validEmail, validPassword)

        params = {'username': validUsername, 'password': validPassword}
        self.client.post("/login/", data=params)
        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated())

    def test_unregisteredUserCannotLogIn(self):
        params = {'username': validUsername, 'password': validPassword}
        self.client.post("/login/", data=params)
        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated())
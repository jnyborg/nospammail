from settings_console.models import GeneratedEmail
from login.tests import *
from settings_console.views import get_user_emails, EmailVisiblity

def addEmail(self, description=None):

    _email = description if description is not None else validEmailDescription

    return self.client.get("/ajax/add_email/", data={'description': _email})

def toggleEmail(self, id):

    return self.client.get("/ajax/toggle_email/", data={'id': id})

class TestEmailGeneration(TestCase):

    def test_shouldBeAbleToGenerateEmailWhileLoggedIn(self):
        """
        Users should be able to generate a new email once logged in 
        """

        registerAndLogin(self)

        addEmail(self, description=validEmailDescription)

        emails = GeneratedEmail.objects.all()

        self.assertTrue(len(emails) == 1, "Failed to generate email")

    def test_generatedEmailShouldBeAssignedCorrectUserId(self):
        """
        Emails generated should be assigned the correct user id
        """

        registerAndLogin(self)

        addEmail(self, description=validEmailDescription)

        user = auth.get_user(self.client)
        emails = GeneratedEmail.objects.filter(user_id=user.id)

        self.assertTrue(len(emails) == 1, "User id was not correct")
    
    def test_shouldNotBeAbleToGenerateEmailWhileNotLoggedIn(self):
        """
        Users should not be able to generate a new email while not logged in
        """

        addEmail(self, description=validEmailDescription)

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
            addEmail(self, description=validEmailDescription)

        emails = GeneratedEmail.objects.all()

        self.assertTrue(len(emails) == 2, "Failed to generate multiple emails with same description")
        self.assertTrue(emails[0].description == emails[1].description, "Emails created with same description had did not have the same description")

    def test_shouldBeAbleToEnableEmail(self):
        """
        Users should be able to enable forwarding of emails
        """

        registerAndLogin(self)

        addEmail(self, description=validEmailDescription)

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

        addEmail(self, description=validEmailDescription)

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

        addEmail(self, description=validEmailDescription)

        logOut(self)

        registerAndLogin(self, username=validUsername2, password=validPassword2, email=validEmail2)

        addEmail(self, description=validEmailDescription)

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

        addEmail(self, description=validEmailDescription)

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

        addEmail(self)

        logOut(self)

        registerAndLogin(self, username=validUsername2, password=validPassword2, email=validEmail2)
        addEmail(self, description=validEmailDescription)

        email1 = GeneratedEmail.objects.all()[0]
        email2 = GeneratedEmail.objects.all()[1]

        self.assertNotEqual(email1.user_id, email2.user_id, "Different users generated emails with same user id")

    def test_shouldNotDisplayHiddenEmails(self):
        """
        Users should be able to hide emails 
        """

        registerAndLogin(self)

        addEmail(self)
        addEmail(self)

        user = auth.get_user(self.client)

        emails = get_user_emails(user, EmailVisiblity.VISIBLE)
        emailLen1 = len(emails)

        emails[0].hidden = True
        emails[0].save()

        emails2 = get_user_emails(user, EmailVisiblity.VISIBLE)
        emailLen2 = len(emails2)

        self.assertNotEqual(emailLen1, emailLen2, "Hiding email did not remove from view")

    def test_shouldNotDisplayDeletedEmails(self):
        """
        Users should be able to hide emails 
        """

        registerAndLogin(self)

        addEmail(self)
        addEmail(self)

        user = auth.get_user(self.client)

        emails = get_user_emails(user, EmailVisiblity.VISIBLE)
        emailLen1 = len(emails)

        emails[0].deleted = True
        emails[0].save()

        emails2 = get_user_emails(user, EmailVisiblity.VISIBLE)
        emailLen2 = len(emails2)

        self.assertNotEqual(emailLen1, emailLen2, "Hiding email did not remove from view")
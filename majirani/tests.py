from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from .views import signup
from .forms import SignUpForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import views as auth_views
from django.core import mail

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import SetPasswordForm


class SignUpTests(TestCase):
    """
    signup tests
    """
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)


class SignUpFormTest(TestCase):
    """
    testing signup form is working
    """
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class SuccessfulSignUpTests(TestCase):
    """
    successful signup tests
    """
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'eugene',
            'email': 'eugenenzioki@gmail.com',
            'password1': 'qwerty123',
            'password2': 'qwerty123'
        }
        self.response = self.client.post(url, data)
        self.edit_profile_url = reverse('edit_profile')

    def test_form_inputs(self):
        """
        testing form input
        :return:
        """
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

    def test_redirection(self):
        """
        testing for redirection to profile edit page upon signup
        """
        self.assertRedirects(self.response, self.edit_profile_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """
        test user authentication

        """
        response = self.client.get(self.edit_profile_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


# invalid signup tests
class InvalidSignUpTests(TestCase):
    """
    testing for signup
    """
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        """
        testing invalid form submission
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())


# Testing password reset
class PasswordResetTests(TestCase):
    """
    class to test password reset
    """
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        """
        testing whether form contain csrf
        :return:
        """
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


# successful password reset
class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'eugenenziokim@gmail.com'
        User.objects.create_user(username='eugene', email=email, password='123abcdef')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        """
        testing redirection of users after password
        """
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


# Invalid password reset test
class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'randomize@email.com'})

    def test_redirection(self):
        """
        testing redirection after password reset
        """
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))


# testing email reset test
class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='eugene', email='eugenenziokim@gmail.com', password='123')
        self.response = self.client.post(reverse('password_reset'), { 'email': 'eugenenziokim@gmail.com' })
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('[CLONEWARS] Please reset your password', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('eugene', self.email.body)
        self.assertIn('eugenenziokim@gmail.com', self.email.body)

    def test_email_to(self):
        self.assertEqual(['eugenenziokim@gmail.com',], self.email.to)


# password reset done
class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)


class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='eugene', email='eugenenziokim@gmail.com', password='123abcdef')

        """
        test creating a valid reset password token
        """
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


# Invalid password reset confirmation
class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='eugene', email='eugenenziokim@gmail.com', password='123abcdef')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)

        """
        testing token invalidation by changing the password
        """
        user.set_password('abcdef123')
        user.save()

        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/complete/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)


class PasswordChangeTestCase(TestCase):
    """
    testing request for password change
    """
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='john', password='old_password')
        self.response = self.client.post(self.url, data)


# testing for successful password change
class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    """
    test for successful password change
    """
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })

    def test_redirection(self):
        """
        testing user redirection after submitting password change form
        :return:
        """
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        """
        refreshing user instance to get new password
        """
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        """
        creating request to a random page upon successful authentication after password change

        """
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

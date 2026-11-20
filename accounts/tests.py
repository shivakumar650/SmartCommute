from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    def test_registration_creates_logged_in_user(self):
        response = self.client.post(reverse("accounts:register"), {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@example.com",
            "password1": "SmartCommute-123",
            "password2": "SmartCommute-123",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_existing_user_can_login_and_invalid_login_is_rejected(self):
        User.objects.create_user(username="commuter", password="SmartCommute-123")

        valid = self.client.post(reverse("accounts:login"), {
            "username": "commuter",
            "password": "SmartCommute-123",
        })
        self.assertRedirects(valid, reverse("commute:dashboard"))

        self.client.logout()
        invalid = self.client.post(reverse("accounts:login"), {
            "username": "commuter",
            "password": "wrong-password",
        })
        self.assertEqual(invalid.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_redirects_home(self):
        User.objects.create_user(username="commuter", password="SmartCommute-123")
        self.client.login(username="commuter", password="SmartCommute-123")

        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(response, reverse("home"))

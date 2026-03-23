from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.existing_user = User.objects.create_user(
            username='existinguser',
            password='TestPass2024!',
            email='existing@test.com'
        )

    def test_user_can_register(self):
        # Test that a new user can register successfully
        data = {
            'username': 'newuser',
            'password': 'NewPass2024!',
            'email': 'newuser@test.com'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_with_existing_username_fails(self):
        # Test that registering with an existing username fails
        data = {
            'username': 'existinguser',
            'password': 'TestPass2024!',
            'email': 'another@test.com'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_login(self):
        # Test that a user can login with correct credentials
        data = {
            'username': 'existinguser',
            'password': 'TestPass2024!'
        }
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_wrong_password_fails(self):
        # Test that login fails with incorrect password
        data = {
            'username': 'existinguser',
            'password': 'WrongPassword!'
        }
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_requires_authentication(self):
        # Test that the profile endpoint requires a logged in user
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_view_profile(self):
        # Test that a logged in user can view their profile
        self.client.force_authenticate(user=self.existing_user)
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')
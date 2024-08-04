from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class AuthTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='testuser@example.com', name='Test User', password='testpass123')
        cls.login_url = reverse('login')
        cls.refresh_url = reverse('refresh')
        cls.logout_url = reverse('logout')
        cls.provider_auth_url = reverse('provider-auth', kwargs={'provider': 'google'})

    def test_user_login(self):
        """Test that a user can log in with valid credentials."""
        response = self.client.post(self.login_url, {'email': self.user.email, 'password': 'testpass123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Login Successful.')
        self.assertIn('access', response.cookies)
        self.assertIn('refresh', response.cookies)
        self.assertIn('logged_in', response.cookies)

    def test_invalid_user_login(self):
        """Test that a user cannot log in with invalid credentials."""
        response = self.client.post(self.login_url, {'email': self.user.email, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')

    def test_token_refresh(self):
        """Test that a user can refresh their token with a valid refresh token."""
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = str(refresh)
        response = self.client.post(self.refresh_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Access tokens refreshed successfully')
        self.assertIn('access', response.cookies)
        self.assertIn('refresh', response.cookies)
        self.assertIn('logged_in', response.cookies)

    def test_invalid_token_refresh(self):
        """Test that a user cannot refresh their token with an invalid refresh token."""
        self.client.cookies['refresh'] = 'invalidtoken'
        response = self.client.post(self.refresh_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Token is invalid or expired')

    def test_user_logout(self):
        """Test that a user can log out and their tokens are cleared."""
        login_response = self.client.post(self.login_url, {'email': self.user.email, 'password': 'testpass123'})
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', self.client.cookies)
        self.assertIn('refresh', self.client.cookies)
        self.assertIn('logged_in', self.client.cookies)
        
        logout_response = self.client.post(self.logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.cookies.get('access').value, '')
        self.assertEqual(self.client.cookies.get('refresh').value, '')
        self.assertEqual(self.client.cookies.get('logged_in').value, '')


class UserRegistrationTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_url = reverse('user-list')
        cls.activation_url = '/api/v1/auth/users/activation/'
        cls.login_url = reverse('login')
        cls.user_data = {
            "name": "Test User",
            "email": "testuser2@example.com",
            "password": "testpass123",
            "re_password": "testpass123"
        }

    def test_user_registration(self):
        """Test that a user can register with valid data."""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(response.data['name'], self.user_data['name'])

    def test_duplicate_user_registration(self):
        """Test that a user cannot register with an email that is already taken."""
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_unactivated_user_cannot_login(self):
        """Test that an unactivated user cannot log in."""
        register_response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        
        login_response = self.client.post(self.login_url, {'email': self.user_data['email'], 'password': self.user_data['password']})
        self.assertEqual(login_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(login_response.data['detail'], 'No active account found with the given credentials')

    def test_user_login(self):
        """Test that a user can log in after activating their account."""
        register_response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', register_response.data)
        self.assertEqual(register_response.data['email'], self.user_data['email'])
        self.assertEqual(register_response.data['name'], self.user_data['name'])
        
        user = User.objects.get(email=self.user_data['email'])
        uid = urlsafe_base64_encode(str(user.pk).encode())  
        token = default_token_generator.make_token(user)

        activation_data = {
            'uid': uid,
            'token': token,
        }
        
        activation_response = self.client.post(self.activation_url, activation_data)
        self.assertEqual(activation_response.status_code, status.HTTP_204_NO_CONTENT)
        
        login_response = self.client.post(self.login_url, {'email': self.user_data['email'], 'password': self.user_data['password']})
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.cookies)
        self.assertIn('refresh', login_response.cookies)
        self.assertIn('logged_in', login_response.cookies)
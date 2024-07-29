from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class AuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', name='Test User', password='testpass123')
        self.login_url = reverse('login')
        self.refresh_url = reverse('refresh')
        self.logout_url = reverse('logout')
        self.provider_auth_url = reverse('provider-auth', kwargs={'provider': 'google'})


    def test_user_login(self):
        response = self.client.post(self.login_url, {'email': 'testuser@example.com', 'password': 'testpass123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Login Successful.')
        self.assertIn('access', response.cookies)
        self.assertIn('refresh', response.cookies)
        self.assertIn('logged_in', response.cookies)
        
        
    def test_invalid_user_login(self):
        response = self.client.post(self.login_url, {'email': 'testuser@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
      
    def test_token_refresh(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh
        response = self.client.post(self.refresh_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Access tokens refreshed successfully')
        self.assertIn('access', response.cookies)
        self.assertIn('refresh', response.cookies)
        self.assertIn('logged_in', response.cookies)


    def test_invalid_token_refresh(self):
        self.client.cookies['refresh'] = 'invalidtoken'
        response = self.client.post(self.refresh_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_user_logout(self):
        # First, log in the user
        login_response = self.client.post(self.login_url, {'email': 'testuser@example.com', 'password': 'testpass123'})
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', self.client.cookies)
        self.assertIn('refresh', self.client.cookies)
        self.assertIn('logged_in', self.client.cookies)
        logout_response = self.client.post(self.logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if cookies are cleared
        self.assertEqual(self.client.cookies.get('access').value, '')
        self.assertEqual(self.client.cookies.get('refresh').value, '')
        self.assertEqual(self.client.cookies.get('logged_in').value, '')

        # Ensure cookies are removed from the response
        self.assertEqual(logout_response.cookies.get('access').value, '')
        self.assertEqual(logout_response.cookies.get('refresh').value, '')
        self.assertEqual(logout_response.cookies.get('logged_in').value, '')
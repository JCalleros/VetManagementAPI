from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode

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
        login_response = self.client.post(self.login_url, {'email': 'testuser@example.com', 'password': 'testpass123'})
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', self.client.cookies)
        self.assertIn('refresh', self.client.cookies)
        self.assertIn('logged_in', self.client.cookies)
        logout_response = self.client.post(self.logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.cookies.get('access').value, '')
        self.assertEqual(self.client.cookies.get('refresh').value, '')
        self.assertEqual(self.client.cookies.get('logged_in').value, '')
        self.assertEqual(logout_response.cookies.get('access').value, '')
        self.assertEqual(logout_response.cookies.get('refresh').value, '')
        self.assertEqual(logout_response.cookies.get('logged_in').value, '')


class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('user-list')
        self.activation_url = '/api/v1/auth/users/activation/'
        self.login_url = reverse('login')
        self.user_data = {
            "name": "Test User",
            "email": "testuser2@example.com",
            "password": "testpass123",
            "re_password": "testpass123"
        }


    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(response.data['name'], self.user_data['name'])


    def test_duplicate_user_registration(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

  
    def test_unactivated_user_cannot_login(self):
        register_response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        
        login_response = self.client.post(self.login_url, {'email': self.user_data['email'], 'password': self.user_data['password']})
        self.assertEqual(login_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(login_response.data['detail'].code, 'no_active_account')

 
    def test_user_login(self):
        register_response  = self.client.post(self.register_url, self.user_data)
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
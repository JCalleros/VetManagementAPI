from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class OwnerCreateTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create test user
        cls.user = User.objects.create_user(email='testuser2@example.com', name="New User", password='testpass123')
        
        # URL endpoints
        cls.login_url = reverse('login')
        cls.owner_create_url = reverse('owner-create')
        
        # Owner data
        cls.owner_data = {
            "name": "Mario",
            "phone_number": "+526647878923"
        }
        
    def setUp(self):
        # Authenticate user and store tokens
        self.authenticated_client = self.client_class()
        self.authenticate()

    def authenticate(self):
        response = self.authenticated_client.post(self.login_url, {'email': 'testuser2@example.com', 'password': 'testpass123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.cookies['access'].value
        self.refresh_token = response.cookies['refresh'].value
        self.logged_in = response.cookies['logged_in'].value

    def add_authentication(self, client):
        client.cookies['access'] = self.access_token
        client.cookies['refresh'] = self.refresh_token
        client.cookies['logged_in'] = self.logged_in

    def test_authenticated_user_can_create_owner(self):
        """Test that an authenticated user can create an owner."""
        self.add_authentication(self.authenticated_client)
        
        response = self.authenticated_client.post(self.owner_create_url, self.owner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.owner_data['name'])
        self.assertEqual(response.data['phone_number'], self.owner_data['phone_number'])

    def test_unauthenticated_user_cannot_create_owner(self):
        """Test that an unauthenticated user cannot create an owner."""
        response = self.client.post(self.owner_create_url, self.owner_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_duplicated_user_phone(self):
        """Test that creating an owner with a duplicated phone number fails."""
        self.add_authentication(self.authenticated_client)
        
        # Create the first owner
        response = self.authenticated_client.post(self.owner_create_url, self.owner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Attempt to create a second owner with the same phone number
        response = self.authenticated_client.post(self.owner_create_url, self.owner_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
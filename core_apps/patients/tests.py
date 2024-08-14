from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class PatientCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='testuser2@example.com', name="New User", password='testpass123')        
        cls.login_url = reverse('login')
        cls.patient_get_all_url = reverse('patient-list')
        cls.owner_create_url = reverse('owner-create')
        cls.patient_create_url = reverse('patient-create')
        cls.owner_data = {"name": "Mario", "phone_number": "+526647878923"}
        cls.patient_data = {
            "name": "Buddy",
            "species": "Dog",
            "gender": "male",
            "breed": "Golden Retriever",
            "age_years": 3,
            "color": "Golden"
        }

    def setUp(self):
        self.client = self.client_class()
        self.authenticate()
        self.owner = self.create_owner()

    def authenticate(self):
        response = self.client.post(self.login_url, {'email': self.user.email, 'password': 'testpass123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.cookies['access'] = response.cookies['access']
        self.client.cookies['refresh'] = response.cookies['refresh']
        self.client.cookies['logged_in'] = response.cookies['logged_in']

    def create_owner(self):
        response = self.client.post(self.owner_create_url, self.owner_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def test_authenticated_user_can_create_patient(self):
        self.patient_data["owner"] = self.owner["id"]
        response = self.client.post(self.patient_create_url, self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.patient_data["name"])

    def test_unauthenticated_user_cannot_create_patient(self):
        self.client.cookies.clear()
        response = self.client.post(self.patient_create_url, self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicated_patient(self):
        self.patient_data["owner"] = self.owner["id"]
        response = self.client.post(self.patient_create_url, self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.post(self.patient_create_url, self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_add_patient_to_owner(self):
        self.patient_data["owner"] = self.owner["id"]
        response = self.client.post(self.patient_create_url, self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        new_patient_data = {
            "name": "Mari",
            "species": "Cat",
            "gender": "female",
            "age_years": 3,
            "owner": self.owner["id"]
        }
        
        response = self.client.post(self.patient_create_url, new_patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], new_patient_data["name"])
        self.assertEqual(response.data["species"], new_patient_data["species"])

    def test_invalid_patient_data(self):
        self.patient_data["owner"] = self.owner["id"]
        self.patient_data["age_years"] = -1
        response = self.client.post(self.patient_create_url, self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("age_years", response.data)
        self.assertEqual(response.data["age_years"], ["Ensure this value is greater than or equal to 0."])

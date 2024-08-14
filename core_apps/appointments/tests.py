from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from core_apps.owners.models import Owner
from core_apps.patients.models import Patient
from .models import Appointment

User = get_user_model()

class AppointmentTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='testuser@example.com', name="Test User", password='testpass123')
        cls.login_url = reverse('login')
        cls.owner_create_url = reverse('owner-create')
        cls.patient_create_url = reverse('patient-create')
        cls.appointment_create_url = reverse('appointment-create')
        cls.owner_data = {"name": "John Doe", "phone_number": "+526647828123"}
        cls.patient_data = {
            "name": "Buddy",
            "species": "Dog",
            "gender": "male",
            "breed": "Golden Retriever",
            "age_years": 3,
            "color": "Golden"
        }
        cls.appointment_data = {
            "date": "2024-07-30T14:30:00Z",
            "service_type": "Vaccination",
            "status": "scheduled",
            "notes": "First vaccination"
        }

    def setUp(self):
        self.client = self.client_class()
        self.authenticate()
        self.owner = self.create_owner()
        self.patient = self.create_patient(self.owner["id"])

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

    def create_patient(self, owner_id):
        self.patient_data["owner"] = owner_id
        response = self.client.post(self.patient_create_url, self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data
    
    def create_appointment(self, patient_id):
        data = self.appointment_data.copy()
        data["patient"] = patient_id
        response = self.client.post(self.appointment_create_url, data)
        return response

    def test_authenticated_user_can_create_appointment(self):
        response = self.create_appointment(self.patient["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["patient"]["id"], self.patient["id"])
        self.assertEqual(response.data["service_type"], self.appointment_data["service_type"])


    def test_duplicate_appointment(self):
        response = self.create_appointment(self.patient["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.create_appointment(self.patient["id"])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_invalid_appointment_data(self):
        data = self.appointment_data.copy()
        data["date"] = "invalid-date"
        data["patient"] = self.patient["id"]
        response = self.client.post(self.appointment_create_url, self.appointment_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)
    
    def test_authenticated_user_can_get_appointment_detail(self):
        response = self.create_appointment(self.patient["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        appointment_id = response.data["id"]

        detail_url = reverse('appointment-detail', kwargs={'id': appointment_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], appointment_id)

        
    def test_authenticated_user_can_delete_appointment(self):
        response = self.create_appointment(self.patient["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        appointment_id = response.data["id"]

        delete_url = reverse('appointment-delete', kwargs={'id': appointment_id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        detail_url = reverse('appointment-detail', kwargs={'id': appointment_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    # Unauthorized tests
    def test_unauthenticated_user_cannot_create_appointment(self):
        self.client.cookies.clear()
        response = self.create_appointment(self.patient["id"])
        response = self.client.post(self.appointment_create_url, self.appointment_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
    def test_authenticated_user_can_get_appointment_detail(self):
        response = self.create_appointment(self.patient["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        appointment_id = response.data["id"]

        detail_url = reverse('appointment-detail', kwargs={'id': appointment_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], appointment_id)
    
    
    def test_unauthenticated_user_cannot_get_appointment_detail(self):
        response = self.create_appointment(self.patient["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        appointment_id = response.data["id"]

        self.client.cookies.clear()
        detail_url = reverse('appointment-detail', kwargs={'id': appointment_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
   
    def test_unauthenticated_user_cannot_delete_appointment(self):
        response = self.create_appointment(self.patient["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        appointment_id = response.data["id"]

        self.client.cookies.clear()
        delete_url = reverse('appointment-delete', kwargs={'id': appointment_id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_update_appointment(self):
        response = self.create_appointment(self.patient["id"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        appointment_id = response.data["id"]

        self.client.cookies.clear()
        update_url = reverse('appointment-update', kwargs={'id': appointment_id})
        update_data = self.appointment_data.copy()
        update_data["status"] = "completed"
        response = self.client.put(update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
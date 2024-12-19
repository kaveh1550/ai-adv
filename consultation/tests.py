from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class ConsultationTests(APITestCase):

    def setUp(self):
        # ایجاد یک کاربر برای تست‌ها
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

    def test_create_consultation(self):
        data = {'topic': 'Legal Advice', 'description': 'Discuss legal matters.'}
        response = self.client.post('/api/v1/create/', data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_consultations(self):
        response = self.client.get('/api/v1/list/', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

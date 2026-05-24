from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()


class AuthTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="1234"
        )

    def test_jwt_login(self):
        response = self.client.post(
            "/api/token/",
            {
                "username": "testuser",
                "password": "1234"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
    
    def test_unauthorized_request(self):
        response = self.client.get("/api/accounts/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
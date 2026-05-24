# users/tests/test_auth.py
import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestUserAuth:
    def test_user_registration(self, api_client):
        url = reverse('user-register')  # измените на ваш URL
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'newuser'

    def test_jwt_token_obtain(self, api_client, user):
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
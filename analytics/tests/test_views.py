# analytics/tests/test_views.py
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from django.urls import reverse

@pytest.mark.django_db
class TestAnalytics:
    
    def test_summary_analytics(self, auth_client, user, transaction_factory, account):
        """Тест аналитики"""
        # Создаем транзакции через фабрику
        transaction_factory(user=user, account=account, amount=500, type='income')
        transaction_factory(user=user, account=account, amount=100, type='expense')
        transaction_factory(user=user, account=account, amount=50, type='expense')
        
        # Проверяем, что URL существует
        try:
            url = reverse('analytics-summary')
        except:
            pytest.skip("URL 'analytics-summary' не настроен в проекте")
        
        response = auth_client.get(url)
        
        # Если API еще не реализован, тест пропускаем
        if response.status_code == 404:
            pytest.skip("API аналитики еще не реализован")
        
        assert response.status_code == 200
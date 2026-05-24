# tests/test_settings.py
import pytest
from django.conf import settings

@pytest.mark.django_db
class TestDjangoSettings:
    """Проверка настроек Django"""
    
    def test_settings_loaded(self):
        """Проверяет, что настройки загрузились"""
        assert hasattr(settings, 'INSTALLED_APPS')
        assert 'rest_framework' in settings.INSTALLED_APPS
    
    def test_database_configured(self):
        """Проверяет настройки базы данных"""
        assert settings.DATABASES['default']['ENGINE'] is not None
# tests/test_django_basic.py
import pytest
from django.test import TestCase
from django.conf import settings

@pytest.mark.django_db
def test_django_settings_loaded():
    """Проверка загрузки настроек Django"""
    assert hasattr(settings, 'INSTALLED_APPS')
    assert 'django.contrib.admin' in settings.INSTALLED_APPS

@pytest.mark.django_db
def test_database_connection():
    """Проверка подключения к БД"""
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        assert cursor.fetchone()[0] == 1

class TestSimpleDjango:
    """Тестовый класс"""
    
    def test_math(self):
        assert 10 / 2 == 5
    
    def test_string(self):
        assert "pytest".upper() == "PYTEST"
# conftest.py (скопируй полностью)
import pytest
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import datetime, timedelta

User = get_user_model()

@pytest.fixture
def user(db):
    """Фикстура пользователя"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def currency(db):
    """Фикстура валюты"""
    from currency.models import Currency
    currency, _ = Currency.objects.get_or_create(
        code='RUB',
        defaults={'name': 'Russian Ruble', 'symbol': '₽'}
    )
    return currency

@pytest.fixture
def account(db, user, currency):
    """Фикстура счета (Account)"""
    from accounts.models import Account
    return Account.objects.create(
        user=user,
        name='Test Account',  # 👈 поле name обязательно! (есть в модели? добавил)
        type='bank',  # 👈 одно из ACCOUNT_TYPES
        balance=Decimal('10000.00'),
        currency=currency,  # 👈 это объект Currency
        is_active=True
    )

@pytest.fixture
def category(db, user):
    """Фикстура категории"""
    from categories.models import Category
    return Category.objects.create(
        name='Test Category',
        type='expense',
        user=user
    )

@pytest.fixture
def transaction_factory(db, user, account, category):
    """Фабрика транзакций"""
    from transactions.models import Transaction
    
    def create_transaction(**kwargs):
        defaults = {
            'user': user,
            'account': account,  # 👈 обязательно
            'category': category,
            'amount': Decimal('100.00'),
            'description': 'Test transaction',
            'type': 'expense',
            'date': datetime.now().date(),
        }
        defaults.update(kwargs)
        return Transaction.objects.create(**defaults)
    
    return create_transaction

@pytest.fixture
def bank_connection(db, user):
    """Фикстура подключения к банку (BankConnection)"""
    from integrations.models import BankConnection
    
    return BankConnection.objects.create(
        user=user,
        bank_name='tinkoff',
        access_token='encrypted_test_token',
        refresh_token='encrypted_test_refresh_token',  # 👈 обязательно
        token_expires_at=datetime.now() + timedelta(days=30),
        last_sync=None,
        is_active=True
    )

@pytest.fixture
def api_client():
    """API клиент"""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def auth_client(api_client, user):
    """Авторизованный клиент"""
    from rest_framework_simplejwt.tokens import AccessToken
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {AccessToken.for_user(user)}')
    return api_client
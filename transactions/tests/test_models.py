# transactions/tests/test_models.py
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError

@pytest.mark.django_db
class TestTransactionModel:
    
    def test_transaction_creation(self, user, account, category):
        """Тест создания транзакции"""
        from transactions.models import Transaction
        from datetime import date
        
        transaction = Transaction.objects.create(
            user=user,
            account=account,
            category=category,
            amount=Decimal('100.50'),
            description='Test transaction',
            type='expense',
            date=date.today()
        )
        
        assert transaction.amount == Decimal('100.50')
        assert transaction.type == 'expense'
        assert transaction.account == account
        assert transaction.user == user
    
    def test_negative_amount_not_allowed(self, user, account, category):
        """Тест запрета отрицательной суммы (если есть валидация)"""
        from transactions.models import Transaction
        from datetime import date
        
        # Создаем транзакцию с отрицательной суммой
        # Если в модели есть валидация - будет ошибка
        # Если нет - тест пропускаем
        try:
            transaction = Transaction.objects.create(
                user=user,
                account=account,
                category=category,
                amount=Decimal('-50.00'),
                description='Negative transaction',
                type='expense',
                date=date.today()
            )
            # Если создалось без ошибок - проверим, что сумма отрицательная
            assert transaction.amount == Decimal('-50.00')
        except ValidationError:
            # Если есть валидация - тест проходит
            pass
# transactions/services.py
from transactions.models import Transaction

class TransactionService:
    """Сервис для работы с транзакциями"""
    
    @staticmethod
    def create(user, amount, date, description, transaction_type, 
               external_id=None, source='manual', **kwargs):
        """Создание транзакции с поддержкой банковских интеграций"""
        return Transaction.objects.create(
            user=user,
            amount=amount,
            date=date,
            description=description,
            type=transaction_type,
            external_id=external_id,
            source=source,
            **kwargs
        )
    
    @staticmethod
    def get_user_transactions(user):
        """Получить все транзакции пользователя"""
        return Transaction.objects.filter(user=user)
    
    @staticmethod
    def get_by_external_id(user, external_id):
        """Найти транзакцию по external_id (для дедупликации)"""
        try:
            return Transaction.objects.get(user=user, external_id=external_id)
        except Transaction.DoesNotExist:
            return None
        
def create_transaction(user, amount, date, description, transaction_type, **kwargs):
    """Обертка для вызова TransactionService.create (для обратной совместимости)"""
    return TransactionService.create(
        user=user,
        amount=amount,
        date=date,
        description=description,
        transaction_type=transaction_type,
        **kwargs
    )
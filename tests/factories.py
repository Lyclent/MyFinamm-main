# tests/factories.py
import factory
from django.contrib.auth import get_user_model
from decimal import Decimal
from transactions.models import Transaction, Category

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpass')

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    name = factory.Sequence(lambda n: f'Category {n}')
    type = 'expense'

class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction
    
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = Decimal('100.00')
    description = factory.Faker('sentence')
    transaction_type = 'expense'
    date = factory.Faker('date_this_year')
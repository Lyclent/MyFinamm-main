from django.test import TestCase
from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from currency.models import Currency
from accounts.models import Account
from categories.models import Category
from subscriptions.models import Subscription

from transactions.services import apply_subscription


User = get_user_model()


class SubscriptionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="1234"
        )

        self.currency = Currency.objects.create(
            code="USD",
            name="Dollar",
            symbol="$"
        )

        self.account = Account.objects.create(
            user=self.user,
            name="Main",
            type="card",
            balance=1000,
            currency=self.currency
        )

        self.category = Category.objects.create(
            user=self.user,
            name="Subscriptions",
            type="expense"
        )

        self.subscription = Subscription.objects.create(
            user=self.user,
            name="Netflix",
            amount=Decimal("100"),
            account=self.account,
            category=self.category,
            period="monthly",
            next_payment_date=date(2025, 1, 1)
        )

    def test_apply_subscription(self):
        apply_subscription(self.subscription)

        self.account.refresh_from_db()

        self.assertEqual(
            self.account.balance,
            Decimal("900")
        )

    def test_subscription_insufficient_funds(self):
        self.account.balance = 10
        self.account.save()

        with self.assertRaises(ValidationError):
            apply_subscription(self.subscription)
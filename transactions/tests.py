from django.test import TestCase

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from currency.models import Currency
from accounts.models import Account

from transactions.services import (
    create_transaction,
    transfer_money,
)


User = get_user_model()


class TransactionServiceTest(TestCase):

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
            name="Main Card",
            type="card",
            balance=1000,
            currency=self.currency
        )

        self.second_account = Account.objects.create(
            user=self.user,
            name="Cash",
            type="cash",
            balance=500,
            currency=self.currency
        )

    def test_expense_transaction(self):
        create_transaction(
            user=self.user,
            type="expense",
            account=self.account,
            amount=Decimal("100")
        )

        self.account.refresh_from_db()

        self.assertEqual(
            self.account.balance,
            Decimal("900")
        )

    def test_income_transaction(self):
        create_transaction(
            user=self.user,
            type="income",
            account=self.account,
            amount=Decimal("200")
        )

        self.account.refresh_from_db()

        self.assertEqual(
            self.account.balance,
            Decimal("1200")
        )

    def test_transfer_money(self):
        transfer_money(
            user=self.user,
            from_account=self.account,
            to_account=self.second_account,
            amount=Decimal("300")
        )

        self.account.refresh_from_db()
        self.second_account.refresh_from_db()

        self.assertEqual(
            self.account.balance,
            Decimal("700")
        )

        self.assertEqual(
            self.second_account.balance,
            Decimal("800")
        )

    def test_insufficient_funds(self):
        with self.assertRaises(ValidationError):
            create_transaction(
                user=self.user,
                type="expense",
                account=self.account,
                amount=Decimal("5000")
            )

    def test_negative_amount(self):
        with self.assertRaises(ValidationError):
            create_transaction(
                user=self.user,
                type="income",
                account=self.account,
                amount=Decimal("-100")
            )
from transactions.models import Transaction


def get_user_transactions(user):
    return Transaction.objects.filter(user=user)


def get_user_expenses(user):
    return Transaction.objects.filter(user=user, type="expense")
from transactions.models import Transaction


def import_transactions(user, transactions):
    """
    Импортирует транзакции из банка.
    """

    created = 0

    for txn in transactions:

        if Transaction.objects.filter(
            external_id=txn["external_id"]
        ).exists():
            continue

        Transaction.objects.create(
            owner=user,
            type=txn["type"],
            amount=txn["amount"],
            description=txn["description"],
            date=txn["date"],
            external_id=txn["external_id"],
            source="bank_tinkoff"
        )

        created += 1

    return created
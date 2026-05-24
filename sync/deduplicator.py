from transactions.models import Transaction

def is_duplicate(user, external_id: str) -> bool:
    if not external_id:
        return False
    
    return Transaction.objects.filter(
        user=user,
        external_id=external_id
    ).exists()
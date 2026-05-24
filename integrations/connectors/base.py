from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict

class BaseBankConnector(ABC):

    def __init__(self, access_token: str, user_id: int):
        self.access_token = access_token
        self.user_id = user_id
    
    @abstractmethod
    def get_transactions(self, from_date: datetime, to_date: datetime) -> List[Dict]:
        pass
    
    @abstractmethod
    def refresh_token(self) -> str:
        pass
    
    def normalize(self, raw_transaction: Dict) -> Dict:
        return {
            'external_id': '',
            'date': None,
            'amount': 0,
            'description': '',
            'type': '',
            'currency': 'RUB',
        }
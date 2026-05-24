import requests
from datetime import datetime
from typing import List, Dict
from .base import BaseBankConnector

class TinkoffConnector(BaseBankConnector):
    API_URL = "https://business.tinkoff.ru/openapi"
    
    def get_transactions(self, from_date: datetime, to_date: datetime) -> List[Dict]:
        accounts = self._get_accounts()
        
        all_transactions = []
        for account in accounts:
            url = f"{self.API_URL}/api/v1/accounts/{account['id']}/transactions"
            headers = {'Authorization': f'Bearer {self.access_token}'}
            params = {
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d')
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                all_transactions.extend(data.get('items', []))
            elif response.status_code == 401:
                self.refresh_token()
                return self.get_transactions(from_date, to_date)  # рекурсивный повтор
        
        return all_transactions
    
    def _get_accounts(self) -> List[Dict]:
        url = f"{self.API_URL}/api/v1/accounts"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('items', [])
        return []
    
    def refresh_token(self) -> str:
        url = f"{self.API_URL}/api/v1/token/refresh"
        payload = {'refresh_token': self.refresh_token}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            new_token = response.json()['access_token']
            self.access_token = new_token
            return new_token
        raise Exception("Failed to refresh token")
    
    def normalize(self, raw_txn: Dict) -> Dict:
        amount = float(raw_txn.get('amount', 0)) / 100
        
        return {
            'external_id': str(raw_txn.get('id')),
            'date': datetime.fromisoformat(raw_txn.get('date', '').replace('Z', '+00:00')),
            'amount': abs(amount),
            'description': raw_txn.get('description', 'Без описания'),
            'type': 'expense' if amount < 0 else 'income',
            'currency': raw_txn.get('currency', 'RUB'),
            'account_id': raw_txn.get('accountId'),
        }
from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import BankConnection
from .connectors.tinkoff import TinkoffConnector
from .services.sync_service import import_transactions

class ConnectBankView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        bank_name = request.data.get("bank_name")
        access_token = request.data.get("access_token")
        refresh_token = request.data.get("refresh_token")

        connection, created = BankConnection.objects.update_or_create(
            user=request.user,
            bank_name=bank_name,
            defaults={
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_expires_at": timezone.now() + timedelta(days=30),
                "is_active": True,
            }
        )

        return Response({
            "success": True,
            "created": created
        })
    
class SyncBankView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        connection = BankConnection.objects.filter(
            user=request.user,
            is_active=True
        ).first()

        if not connection:
            return Response({
                "error": "Банк не подключен"
            }, status=400)

        connector = TinkoffConnector()

        connector.access_token = connection.access_token

        transactions = connector.get_transactions(
            timezone.now() - timedelta(days=30),
            timezone.now()
        )

        normalized = [
            connector.normalize(txn)
            for txn in transactions
        ]

        created_count = import_transactions(
            request.user,
            normalized
        )

        connection.last_sync = timezone.now()
        connection.save()

        return Response({
            "success": True,
            "transactions_found": len(normalized),
            "transactions_created": created_count
        })
    
class SyncStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        connection = BankConnection.objects.filter(
            user=request.user
        ).first()

        if not connection:
            return Response({
                "connected": False
            })

        return Response({
            "connected": True,
            "bank": connection.bank_name,
            "last_sync": connection.last_sync
        })
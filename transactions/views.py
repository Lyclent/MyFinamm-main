from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from transactions.services import create_transaction


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        create_transaction(
            user=self.request.user,
            **serializer.validated_data
        )
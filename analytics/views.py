from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from transactions.models import Transaction
from accounts.models import Account

class SummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        income = (
            Transaction.objects.filter(
                user=user,
                type="income"
            ).aggregate(total=Sum("amount"))["total"] or 0
        )

        expenses = (
            Transaction.objects.filter(
                user=user,
                type="expense"
            ).aggregate(total=Sum("amount"))["total"] or 0
        )

        balance = (
            Account.objects.filter(
                user=user
            ).aggregate(total=Sum("balance"))["total"] or 0
        )

        return Response({
            "income": income,
            "expenses": expenses,
            "balance": balance,
        })
    
class MonthlyExpensesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        current_month = now().month
        current_year = now().year

        expenses = (
            Transaction.objects.filter(
                user=user,
                type="expense",
                date__month=current_month,
                date__year=current_year
            ).aggregate(total=Sum("amount"))["total"] or 0
        )

        return Response({
            "month": current_month,
            "year": current_year,
            "expenses": expenses,
        })
    
class TopCategoriesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        categories = (
            Transaction.objects.filter(
                user=user,
                type="expense"
            )
            .values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")[:5]
        )

        return Response(categories)
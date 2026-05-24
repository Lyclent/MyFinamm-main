from django.urls import path

from analytics.views import (
    SummaryAPIView,
    MonthlyExpensesAPIView,
    TopCategoriesAPIView,
)

urlpatterns = [
    path("summary/", SummaryAPIView.as_view()),
    path("monthly-expenses/", MonthlyExpensesAPIView.as_view()),
    path("top-categories/", TopCategoriesAPIView.as_view()),
]
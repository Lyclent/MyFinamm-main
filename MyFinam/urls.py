"""
URL configuration for MyFinam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import UserRegistrationView

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import AccountViewSet
from transactions.views import TransactionViewSet
from categories.views import CategoryViewSet
from budgets.views import BudgetViewSet
from goals.views import GoalViewSet
from subscriptions.views import SubscriptionViewSet
from notifications.views import NotificationViewSet
from currency.views import CurrencyViewSet


router = DefaultRouter()

router.register(r'accounts', AccountViewSet, basename='accounts')
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'budgets', BudgetViewSet, basename='budgets')
router.register(r'goals', GoalViewSet, basename='goals')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'currency', CurrencyViewSet, basename='currency')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path("api/analytics/", include("analytics.urls")),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        "api/integrations/",
        include("integrations.urls")
    ),
]
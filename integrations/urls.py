from django.urls import path

from .views import (
    ConnectBankView,
    SyncBankView,
    SyncStatusView
)

urlpatterns = [
    path(
        "connect/",
        ConnectBankView.as_view(),
        name="connect-bank"
    ),

    path(
        "sync/",
        SyncBankView.as_view(),
        name="sync-bank"
    ),

    path(
        "status/",
        SyncStatusView.as_view(),
        name="sync-status"
    ),
]
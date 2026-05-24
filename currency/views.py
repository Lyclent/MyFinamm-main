from rest_framework.viewsets import ReadOnlyModelViewSet

from currency.models import Currency
from currency.serializers import CurrencySerializer


class CurrencyViewSet(ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
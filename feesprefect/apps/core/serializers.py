from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers


class MoneyFieldSerializer(serializers.Serializer):
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency="NGN")

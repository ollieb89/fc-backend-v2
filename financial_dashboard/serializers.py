# financial_dashboard/serializers.py

from rest_framework import serializers
from .models import (
    User,
    FinancialInstitution,
    UserAccount,
    Transaction,
    Category,
    Budget,
    InvestmentHolding,
    CryptoWallet,
    AIInsight,
    Notification,
    AuditLog,
    APIConnection,
    MLModel,
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FinancialInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialInstitution
        fields = '__all__'

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class InvestmentHoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentHolding
        fields = '__all__'

class CryptoWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoWallet
        fields = '__all__'

class AIInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIInsight
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class APIConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIConnection
        fields = '__all__'

class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = '__all__'

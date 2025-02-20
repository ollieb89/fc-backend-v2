from rest_framework import serializers
from.models import (
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
        fields = ['id', 'email', 'first_name', 'last_name', 'created_at']  # Include relevant fields

class FinancialInstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialInstitution
        fields = ['id', 'name', 'institution_type', 'country', 'logo_url']  # Include relevant fields

class UserAccountSerializer(serializers.ModelSerializer):
    institution = FinancialInstitutionSerializer()  # Nested serializer for institution details

    class Meta:
        model = UserAccount
        fields = ['id', 'account_name', 'official_name', 'account_type', 'currency',
                  'balance_current', 'balance_available', 'last_updated', 'institution']

class TransactionSerializer(serializers.ModelSerializer):
    account = UserAccountSerializer()  # Nested serializer for account details
    category = serializers.StringRelatedField()  # Display category name instead of ID

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'amount', 'currency', 'date', 'pending', 'description',
                  'merchant_name', 'category', 'location', 'payment_channel', 'transaction_type']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category', 'is_custom', 'color_code', 'icon_name',
                  'spending_limit', 'type']

class BudgetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested serializer for category details

    class Meta:
        model = Budget
        fields = ['id', 'category', 'amount', 'period', 'start_date', 'end_date',
                  'current_spending', 'currency', 'notifications_enabled']

    def validate(self, data):
        # Example custom validation:
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date cannot be after end date.")
        return data

class InvestmentHoldingSerializer(serializers.ModelSerializer):
    account = UserAccountSerializer()  # Nested serializer for account details

    class Meta:
        model = InvestmentHolding
        fields = ['id', 'account', 'security_name', 'symbol', 'quantity', 'purchase_price',
                  'current_value', 'purchase_date', 'asset_type', 'dividend_yield', 'sector']

class CryptoWalletSerializer(serializers.ModelSerializer):
    exchange = FinancialInstitutionSerializer()  # Nested serializer for exchange details

    class Meta:
        model = CryptoWallet
        fields = ['id', 'exchange', 'public_address', 'coin_type', 'balance', 'last_updated', 'is_hot_wallet']
        extra_kwargs = {'private_key_hash': {'write_only': True}}  # Hide private key hash from responses

class AIInsightSerializer(serializers.ModelSerializer):
    linked_account = UserAccountSerializer()  # Nested serializer for linked account
    linked_transaction = TransactionSerializer()  # Nested serializer for linked transaction

    class Meta:
        model = AIInsight
        fields = ['id', 'generated_at', 'insight_type', 'content', 'confidence_score',
                  'action_items', 'linked_account', 'linked_transaction', 'status', 'feedback_score']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'created_at', 'type', 'content', 'is_read', 'priority_level',
                  'action_url', 'expiration_date']

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ['id', 'ip_address', 'event_type', 'event_timestamp', 'affected_table',
                  'record_id', 'before_state', 'after_state', 'device_fingerprint']

class APIConnectionSerializer(serializers.ModelSerializer):
    institution = FinancialInstitutionSerializer()  # Nested serializer for institution details

    class Meta:
        model = APIConnection
        fields = ['id', 'institution', 'last_successful_sync', 'error_count']
        extra_kwargs = {'access_token': {'write_only': True},
                        'refresh_token': {'write_only': True},
                        'consent_expiry': {'write_only': True}}  # Hide sensitive fields

class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = ['id', 'model_type', 'version', 'training_data_range', 'accuracy_score', 'deployed_at', 'active']
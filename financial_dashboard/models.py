import uuid
from django.db import models
from django.utils import timezone

# 1. Users Table
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    last_login = models.DateTimeField(null=True, blank=True)
    subscription_plan = models.CharField(max_length=50, blank=True)
    timezone = models.CharField(max_length=50, blank=True)
    two_factor_enabled = models.BooleanField(default=False)
    profile_image_url = models.URLField(blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Add is_active field

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email


# 2. Financial Institutions Table
class FinancialInstitution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    institution_type = models.CharField(max_length=50)  # bank, crypto, exchange, etc.
    country = models.CharField(max_length=100)
    base_url = models.URLField()
    logo_url = models.URLField(blank=True)
    auth_type = models.CharField(max_length=50)  # OAuth, API-key, etc.
    api_documentation_url = models.URLField(blank=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'financial_institutions'

    def __str__(self):
        return self.name


# 3. User Accounts Table
class UserAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    institution = models.ForeignKey(FinancialInstitution, on_delete=models.CASCADE, related_name='accounts')
    account_name = models.CharField(max_length=255)
    official_name = models.CharField(max_length=255, blank=True)
    account_type = models.CharField(max_length=50)  # checking, savings, crypto, etc.
    currency = models.CharField(max_length=3)
    balance_current = models.DecimalField(max_digits=18, decimal_places=8)
    balance_available = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)  # Automatically update on each save
    is_hidden = models.BooleanField(default=False)
    plaid_item_id = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'user_accounts'
        indexes = [
            models.Index(fields=['user']),  # Add index for user field
        ]

    def __str__(self):
        return self.account_name


# 4. Transactions Table
class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    currency = models.CharField(max_length=3)
    date = models.DateTimeField()
    pending = models.BooleanField(default=False)
    description = models.TextField()
    merchant_name = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    location = models.CharField(max_length=255, blank=True)
    payment_channel = models.CharField(max_length=50, blank=True)  # online, in-store, etc.
    transaction_type = models.CharField(max_length=10)  # debit or credit
    crypto_exchange_rate = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)

    class Meta:
        db_table = 'transactions'
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['account']),  # Add index for account field
        ]

    def __str__(self):
        return f"{self.description} ({self.amount})"


# 5. Categories Table
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')
    is_custom = models.BooleanField(default=False)
    color_code = models.CharField(max_length=20, blank=True)
    icon_name = models.CharField(max_length=50, blank=True)
    spending_limit = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    type = models.CharField(max_length=10)  # income or expense

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name


# 6. Budgets Table
class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    period = models.CharField(max_length=20)  # weekly, monthly, quarterly, etc.
    start_date = models.DateField()
    end_date = models.DateField()
    current_spending = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    currency = models.CharField(max_length=3)
    notifications_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'budgets'
        indexes = [
            models.Index(fields=['user']),  # Add index for user field
            models.Index(fields=['category']),  # Add index for category field
        ]

    def __str__(self):
        return f"Budget for {self.user} - {self.category}"


# 7. Investment Holdings Table
class InvestmentHolding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='investment_holdings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investment_holdings')
    security_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    purchase_price = models.DecimalField(max_digits=18, decimal_places=8)
    current_value = models.DecimalField(max_digits=18, decimal_places=8)
    purchase_date = models.DateField()
    asset_type = models.CharField(max_length=20)  # stock, bond, ETF, etc.
    dividend_yield = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    sector = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'investment_holdings'
        indexes = [
            models.Index(fields=['user']),  # Add index for user field
            models.Index(fields=['account']),  # Add index for account field
        ]

    def __str__(self):
        return self.symbol


# 8. Crypto Wallets Table
class CryptoWallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_wallets')
    exchange = models.ForeignKey(FinancialInstitution, on_delete=models.CASCADE, related_name='crypto_wallets')
    public_address = models.CharField(max_length=255)
    private_key_hash = models.CharField(max_length=255)  # Ensure strong hashing algorithm is used
    coin_type = models.CharField(max_length=10)
    balance = models.DecimalField(max_digits=18, decimal_places=8)
    last_updated = models.DateTimeField(auto_now=True)  # Automatically update on each save
    is_hot_wallet = models.BooleanField(default=True)

    class Meta:
        db_table = 'crypto_wallets'
        indexes = [
            models.Index(fields=['user']),  # Add index for user field
        ]

    def __str__(self):
        return f"{self.coin_type} Wallet for {self.user}"


# 9. AI Insights Table
class AIInsight(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_insights')
    generated_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    insight_type = models.CharField(max_length=50)  # spending, investment, debt, etc.
    content = models.TextField()
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)
    action_items = models.TextField(blank=True)
    linked_account = models.ForeignKey(UserAccount, null=True, blank=True, on_delete=models.SET_NULL, related_name='insights')
    linked_transaction = models.ForeignKey(Transaction, null=True, blank=True, on_delete=models.SET_NULL, related_name='insights')
    status = models.CharField(max_length=20)  # implemented, dismissed, etc.
    feedback_score = models.IntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)  # Add last_modified field

    class Meta:
        db_table = 'ai_insights'
        indexes = [
            models.Index(fields=['user']),  # Add index for user field
        ]

    def __str__(self):
        return f"AI Insight for {self.user}"


# 10. Notifications Table
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    type = models.CharField(max_length=20)  # budget_alert, security, insight, etc.
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    priority_level = models.IntegerField(default=0)
    action_url = models.URLField(blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        indexes = [
            models.Index(fields=['user']),  # Add index for user field
        ]

    def __str__(self):
        return f"Notification for {self.user}"


# 11. Audit Logs Table
class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    ip_address = models.GenericIPAddressField()
    event_type = models.CharField(max_length=50)
    event_timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    affected_table = models.CharField(max_length=100, blank=True)
    record_id = models.UUIDField(null=True, blank=True)
    before_state = models.JSONField(null=True, blank=True)
    after_state = models.JSONField(null=True, blank=True)
    device_fingerprint = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'audit_logs'
        indexes = [
            models.Index(fields=['user']),  # Add index for user field
        ]

    def __str__(self):
        return f"Audit Log for {self.user}"


# 12. API Connections Table (External API Integration)
class APIConnection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_connections')
    institution = models.ForeignKey(FinancialInstitution, on_delete=models.CASCADE, related_name='api_connections')
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True)
    consent_expiry = models.DateTimeField(null=True, blank=True)
    last_successful_sync = models.DateTimeField(null=True, blank=True)
    error_count = models.IntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)  # Add last_modified field

    class Meta:
        db_table = 'api_connections'
        indexes = [
            models.Index(fields=['user']),  # Add index for user field
        ]

    def __str__(self):
        return f"API Connection for {self.user}"


# 13. ML Models Tracking Table
class MLModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_type = models.CharField(max_length=50)  # e.g., spending analysis, investment recommendations
    version = models.CharField(max_length=20)
    training_data_range = models.CharField(max_length=50)  # alternatively, you could use a DateRangeField if available
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=2)
    deployed_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'ml_models'

    def __str__(self):
        return f"ML Model {self.model_type} v{self.version}"
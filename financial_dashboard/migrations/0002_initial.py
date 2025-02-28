# Generated by Django 5.0.11 on 2025-02-20 19:03

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("financial_dashboard", "0001_enable_uuid_ossp"),
    ]

    operations = [
        migrations.CreateModel(
            name="FinancialInstitution",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("institution_type", models.CharField(max_length=50)),
                ("country", models.CharField(max_length=100)),
                ("base_url", models.URLField()),
                ("logo_url", models.URLField(blank=True)),
                ("auth_type", models.CharField(max_length=50)),
                ("api_documentation_url", models.URLField(blank=True)),
                ("last_sync", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "financial_institutions",
            },
        ),
        migrations.CreateModel(
            name="MLModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("model_type", models.CharField(max_length=50)),
                ("version", models.CharField(max_length=20)),
                ("training_data_range", models.CharField(max_length=50)),
                ("accuracy_score", models.DecimalField(decimal_places=2, max_digits=5)),
                ("deployed_at", models.DateTimeField(auto_now_add=True)),
                ("active", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "ml_models",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("password_hash", models.CharField(max_length=255)),
                ("first_name", models.CharField(blank=True, max_length=100)),
                ("last_name", models.CharField(blank=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                ("subscription_plan", models.CharField(blank=True, max_length=50)),
                ("timezone", models.CharField(blank=True, max_length=50)),
                ("two_factor_enabled", models.BooleanField(default=False)),
                ("profile_image_url", models.URLField(blank=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "users",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("is_custom", models.BooleanField(default=False)),
                ("color_code", models.CharField(blank=True, max_length=20)),
                ("icon_name", models.CharField(blank=True, max_length=50)),
                (
                    "spending_limit",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=18, null=True
                    ),
                ),
                ("type", models.CharField(max_length=10)),
                (
                    "parent_category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="subcategories",
                        to="financial_dashboard.category",
                    ),
                ),
            ],
            options={
                "db_table": "categories",
            },
        ),
        migrations.CreateModel(
            name="UserAccount",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("account_name", models.CharField(max_length=255)),
                ("official_name", models.CharField(blank=True, max_length=255)),
                ("account_type", models.CharField(max_length=50)),
                ("currency", models.CharField(max_length=3)),
                (
                    "balance_current",
                    models.DecimalField(decimal_places=8, max_digits=18),
                ),
                (
                    "balance_available",
                    models.DecimalField(
                        blank=True, decimal_places=8, max_digits=18, null=True
                    ),
                ),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("is_hidden", models.BooleanField(default=False)),
                ("plaid_item_id", models.CharField(blank=True, max_length=255)),
                (
                    "institution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accounts",
                        to="financial_dashboard.financialinstitution",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accounts",
                        to="financial_dashboard.user",
                    ),
                ),
            ],
            options={
                "db_table": "user_accounts",
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=8, max_digits=18)),
                ("currency", models.CharField(max_length=3)),
                ("date", models.DateTimeField()),
                ("pending", models.BooleanField(default=False)),
                ("description", models.TextField()),
                ("merchant_name", models.CharField(blank=True, max_length=255)),
                ("location", models.CharField(blank=True, max_length=255)),
                ("payment_channel", models.CharField(blank=True, max_length=50)),
                ("transaction_type", models.CharField(max_length=10)),
                (
                    "crypto_exchange_rate",
                    models.DecimalField(
                        blank=True, decimal_places=8, max_digits=18, null=True
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="transactions",
                        to="financial_dashboard.category",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="financial_dashboard.user",
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="financial_dashboard.useraccount",
                    ),
                ),
            ],
            options={
                "db_table": "transactions",
            },
        ),
        migrations.CreateModel(
            name="InvestmentHolding",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("security_name", models.CharField(max_length=255)),
                ("symbol", models.CharField(max_length=20)),
                ("quantity", models.DecimalField(decimal_places=8, max_digits=18)),
                (
                    "purchase_price",
                    models.DecimalField(decimal_places=8, max_digits=18),
                ),
                ("current_value", models.DecimalField(decimal_places=8, max_digits=18)),
                ("purchase_date", models.DateField()),
                ("asset_type", models.CharField(max_length=20)),
                (
                    "dividend_yield",
                    models.DecimalField(
                        blank=True, decimal_places=4, max_digits=18, null=True
                    ),
                ),
                ("sector", models.CharField(blank=True, max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="investment_holdings",
                        to="financial_dashboard.user",
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="investment_holdings",
                        to="financial_dashboard.useraccount",
                    ),
                ),
            ],
            options={
                "db_table": "investment_holdings",
            },
        ),
        migrations.CreateModel(
            name="AIInsight",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("generated_at", models.DateTimeField(auto_now_add=True)),
                ("insight_type", models.CharField(max_length=50)),
                ("content", models.TextField()),
                (
                    "confidence_score",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                ("action_items", models.TextField(blank=True)),
                ("status", models.CharField(max_length=20)),
                ("feedback_score", models.IntegerField(blank=True, null=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "linked_transaction",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="insights",
                        to="financial_dashboard.transaction",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ai_insights",
                        to="financial_dashboard.user",
                    ),
                ),
                (
                    "linked_account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="insights",
                        to="financial_dashboard.useraccount",
                    ),
                ),
            ],
            options={
                "db_table": "ai_insights",
            },
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("type", models.CharField(max_length=20)),
                ("content", models.TextField()),
                ("is_read", models.BooleanField(default=False)),
                ("priority_level", models.IntegerField(default=0)),
                ("action_url", models.URLField(blank=True)),
                ("expiration_date", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to="financial_dashboard.user",
                    ),
                ),
            ],
            options={
                "db_table": "notifications",
                "indexes": [
                    models.Index(fields=["user"], name="notificatio_user_id_e78525_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="CryptoWallet",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("public_address", models.CharField(max_length=255)),
                ("private_key_hash", models.CharField(max_length=255)),
                ("coin_type", models.CharField(max_length=10)),
                ("balance", models.DecimalField(decimal_places=8, max_digits=18)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("is_hot_wallet", models.BooleanField(default=True)),
                (
                    "exchange",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="crypto_wallets",
                        to="financial_dashboard.financialinstitution",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="crypto_wallets",
                        to="financial_dashboard.user",
                    ),
                ),
            ],
            options={
                "db_table": "crypto_wallets",
                "indexes": [
                    models.Index(fields=["user"], name="crypto_wall_user_id_9095ed_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="Budget",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=18)),
                ("period", models.CharField(max_length=20)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "current_spending",
                    models.DecimalField(decimal_places=2, default=0, max_digits=18),
                ),
                ("currency", models.CharField(max_length=3)),
                ("notifications_enabled", models.BooleanField(default=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="budgets",
                        to="financial_dashboard.category",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="budgets",
                        to="financial_dashboard.user",
                    ),
                ),
            ],
            options={
                "db_table": "budgets",
                "indexes": [
                    models.Index(fields=["user"], name="budgets_user_id_300e09_idx"),
                    models.Index(
                        fields=["category"], name="budgets_categor_d644d8_idx"
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("ip_address", models.GenericIPAddressField()),
                ("event_type", models.CharField(max_length=50)),
                ("event_timestamp", models.DateTimeField(auto_now_add=True)),
                ("affected_table", models.CharField(blank=True, max_length=100)),
                ("record_id", models.UUIDField(blank=True, null=True)),
                ("before_state", models.JSONField(blank=True, null=True)),
                ("after_state", models.JSONField(blank=True, null=True)),
                ("device_fingerprint", models.CharField(blank=True, max_length=255)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="audit_logs",
                        to="financial_dashboard.user",
                    ),
                ),
            ],
            options={
                "db_table": "audit_logs",
                "indexes": [
                    models.Index(fields=["user"], name="audit_logs_user_id_73c422_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="APIConnection",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("access_token", models.TextField()),
                ("refresh_token", models.TextField(blank=True)),
                ("consent_expiry", models.DateTimeField(blank=True, null=True)),
                ("last_successful_sync", models.DateTimeField(blank=True, null=True)),
                ("error_count", models.IntegerField(default=0)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "institution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="api_connections",
                        to="financial_dashboard.financialinstitution",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="api_connections",
                        to="financial_dashboard.user",
                    ),
                ),
            ],
            options={
                "db_table": "api_connections",
                "indexes": [
                    models.Index(fields=["user"], name="api_connect_user_id_cf21d0_idx")
                ],
            },
        ),
        migrations.AddIndex(
            model_name="useraccount",
            index=models.Index(fields=["user"], name="user_accoun_user_id_cd497a_idx"),
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(
                fields=["user", "date"], name="transaction_user_id_059bf9_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(
                fields=["account"], name="transaction_account_d84ffe_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="investmentholding",
            index=models.Index(fields=["user"], name="investment__user_id_7f80e3_idx"),
        ),
        migrations.AddIndex(
            model_name="investmentholding",
            index=models.Index(
                fields=["account"], name="investment__account_7da236_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="aiinsight",
            index=models.Index(fields=["user"], name="ai_insights_user_id_8fb97d_idx"),
        ),
    ]

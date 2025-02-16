# financial_dashboard/api_urls.py

from rest_framework import routers
from django.urls import path, include
from .api_views import (
    BinanceManualLoginAPIView,
    UserViewSet,
    FinancialInstitutionViewSet,
    UserAccountViewSet,
    TransactionViewSet,
    CategoryViewSet,
    BudgetViewSet,
    InvestmentHoldingViewSet,
    CryptoWalletViewSet,
    AIInsightViewSet,
    NotificationViewSet,
    AuditLogViewSet,
    APIConnectionViewSet,
    MLModelViewSet,
)
from .views import binance_login, binance_callback

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'financial_institutions', FinancialInstitutionViewSet)
router.register(r'user_accounts', UserAccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'investment_holdings', InvestmentHoldingViewSet)
router.register(r'crypto_wallets', CryptoWalletViewSet)
router.register(r'ai_insights', AIInsightViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'audit_logs', AuditLogViewSet)
router.register(r'api_connections', APIConnectionViewSet)
router.register(r'ml_models', MLModelViewSet)

urlpatterns = [
    path('binance/manual-login/', BinanceManualLoginAPIView.as_view(), name='binance-manual-login'),
    path('binance/login/', binance_login, name='binance-login'),
    path('binance/callback/', binance_callback, name='binance-callback'),
    path('', include(router.urls)),
]

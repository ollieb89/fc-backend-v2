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
router.register(r'users', UserViewSet, basename='user')
router.register(r'financial-institutions', FinancialInstitutionViewSet, basename='financial-institution')
router.register(r'user-accounts', UserAccountViewSet, basename='user-account')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'investment-holdings', InvestmentHoldingViewSet, basename='investment-holding')
router.register(r'crypto-wallets', CryptoWalletViewSet, basename='crypto-wallet')
router.register(r'ai-insights', AIInsightViewSet, basename='ai-insight')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')
router.register(r'api-connections', APIConnectionViewSet, basename='api-connection')
router.register(r'ml-models', MLModelViewSet, basename='ml-model')

urlpatterns = [
    path('binance/manual-login/', BinanceManualLoginAPIView.as_view(), name='binance-manual-login'),
    path('binance/login/', binance_login, name='binance-login'),
    path('binance/callback/', binance_callback, name='binance-callback'),
    path('', include(router.urls)),  # Keep this at the end
]
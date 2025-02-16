# financial_dashboard/api_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from binance.client import Client  # Make sure you have installed python-binance
from rest_framework import viewsets
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
from .serializers import (
    UserSerializer,
    FinancialInstitutionSerializer,
    UserAccountSerializer,
    TransactionSerializer,
    CategorySerializer,
    BudgetSerializer,
    InvestmentHoldingSerializer,
    CryptoWalletSerializer,
    AIInsightSerializer,
    NotificationSerializer,
    AuditLogSerializer,
    APIConnectionSerializer,
    MLModelSerializer,
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FinancialInstitutionViewSet(viewsets.ModelViewSet):
    queryset = FinancialInstitution.objects.all()
    serializer_class = FinancialInstitutionSerializer

class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

class InvestmentHoldingViewSet(viewsets.ModelViewSet):
    queryset = InvestmentHolding.objects.all()
    serializer_class = InvestmentHoldingSerializer

class CryptoWalletViewSet(viewsets.ModelViewSet):
    queryset = CryptoWallet.objects.all()
    serializer_class = CryptoWalletSerializer

class AIInsightViewSet(viewsets.ModelViewSet):
    queryset = AIInsight.objects.all()
    serializer_class = AIInsightSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

class APIConnectionViewSet(viewsets.ModelViewSet):
    queryset = APIConnection.objects.all()
    serializer_class = APIConnectionSerializer

class MLModelViewSet(viewsets.ModelViewSet):
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer

class BinanceManualLoginAPIView(APIView):
    """
    API endpoint that accepts Binance API credentials (api_key and api_secret)
    via POST, validates them by retrieving account info, and returns the data in JSON.
    """

    def post(self, request, format=None):
        api_key = request.data.get('api_key')
        api_secret = request.data.get('api_secret')
        if not api_key or not api_secret:
            return Response(
                {"error": "Both 'api_key' and 'api_secret' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Initialize the Binance client with provided credentials
            client = Client(api_key, api_secret)
            # Retrieve account information from Binance
            account_info = client.get_account()
            return Response({"account_info": account_info}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error validating Binance API credentials")
            return Response(
                {"error": f"Error validating credentials: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
# financial_dashboard/api_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
from binance.client import Client
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .models import (
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
from rest_framework.decorators import action

logger = logging.getLogger(__name__)
User = get_user_model()

# Common ViewSet configuration for frontend-ready APIs
class FrontendReadyViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # Set to your preferred pagination class

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data,
            'error': None
        })

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            'success': True,
            'data': response.data,
            'error': None
        })

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        return Response({
            'success': False,
            'data': None,
            'error': {
                'code': response.status_code,
                'message': str(exc)
            }
        }, status=response.status_code)

# Modified ViewSets with frontend-friendly responses
class UserViewSet(FrontendReadyViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        })

class FinancialInstitutionViewSet(FrontendReadyViewSet):
    queryset = FinancialInstitution.objects.all()
    serializer_class = FinancialInstitutionSerializer

class UserAccountViewSet(FrontendReadyViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class TransactionViewSet(FrontendReadyViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_fields = ['account', 'category', 'date']

    def get_queryset(self):
        return self.queryset.filter(account__user=self.request.user)

class CategoryViewSet(FrontendReadyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BudgetViewSet(FrontendReadyViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

class InvestmentHoldingViewSet(FrontendReadyViewSet):
    queryset = InvestmentHolding.objects.all()
    serializer_class = InvestmentHoldingSerializer

class CryptoWalletViewSet(FrontendReadyViewSet):
    queryset = CryptoWallet.objects.all()
    serializer_class = CryptoWalletSerializer

class AIInsightViewSet(FrontendReadyViewSet):
    queryset = AIInsight.objects.all()
    serializer_class = AIInsightSerializer

class NotificationViewSet(FrontendReadyViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class AuditLogViewSet(FrontendReadyViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

class APIConnectionViewSet(FrontendReadyViewSet):
    queryset = APIConnection.objects.all()
    serializer_class = APIConnectionSerializer

class MLModelViewSet(FrontendReadyViewSet):
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer

class BinanceManualLoginAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        """
        Modified to include user association and error handling for frontend
        """
        api_key = request.data.get('api_key')
        api_secret = request.data.get('api_secret')
        
        if not api_key or not api_secret:
            return Response({
                'success': False,
                'data': None,
                'error': {'message': 'Both API key and secret are required'}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Client(api_key, api_secret)
            account_info = client.get_account()
            
            # Store the API connection (example implementation)
            APIConnection.objects.update_or_create(
                user=request.user,
                service_name='binance',
                defaults={'api_key': api_key, 'api_secret': api_secret}
            )

            return Response({
                'success': True,
                'data': {
                    'account_info': account_info,
                    'message': 'Binance connection successful'
                },
                'error': None
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Binance connection error: {str(e)}", exc_info=True)
            return Response({
                'success': False,
                'data': None,
                'error': {
                    'message': 'Failed to connect to Binance',
                    'details': str(e)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
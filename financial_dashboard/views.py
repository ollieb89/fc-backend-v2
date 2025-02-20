import logging

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from.models import Transaction
from.serializers import TransactionSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from.crypto_connectors.binance import BinanceConnector

logger = logging.getLogger(__name__)


def index(request):
    """
    Renders the home page of the financial dashboard.
    """
    return render(request, 'financial_dashboard/index.html')


def dashboard(request):
    """
    Renders the dashboard page.
    """
    return render(request, 'financial_dashboard/dashboard.html')


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Allow any user to access this view
def binance_login(request):
    """
    Redirects the user to Binance's OAuth page.
    """
    connector = BinanceConnector()
    auth_url = connector.get_authorization_url(state="optional_state_value")
    return redirect(auth_url)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Allow any user to access this view
def binance_callback(request):
    """
    Handles Binance's OAuth callback by exchanging the authorization code
    for an access token and retrieving user data.
    """
    code = request.GET.get('code')
    if not code:
        return HttpResponseBadRequest("Authorization code not provided.")

    connector = BinanceConnector()
    try:
        token_data = connector.exchange_code_for_token(code)
        access_token = token_data.get("access_token")
        user_data = connector.get_user_data(access_token)
    except Exception as e:
        logger.exception("Error during Binance OAuth callback:")
        return render(request, "financial_dashboard/binance_callback.html", {"error": str(e)})

    # Here you would integrate the Binance user data with your local user system:
    # For example, find or create a User, store the access token in an APIConnection model, etc.
    context = {
        "token_data": token_data,
        "user_data": user_data,
    }
    return render(request, "financial_dashboard/binance_callback.html", context)


# API view to list and create transactions
class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter transactions to show only those belonging to the logged-in user
        return Transaction.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)  # Automatically set the user field
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# API view to retrieve, update, and delete a transaction
class TransactionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter transactions to show only those belonging to the logged-in user
        return Transaction.objects.filter(user=self.request.user)
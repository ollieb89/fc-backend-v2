# financial_dashboard/views.py

import logging
from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .crypto_connectors.binance import BinanceConnector

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


def binance_login(request):
    """
    Redirects the user to Binance's OAuth page.
    """
    connector = BinanceConnector()
    auth_url = connector.get_authorization_url(state="optional_state_value")
    return redirect(auth_url)

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

# API view to retrieve, update, and delete a transaction
class TransactionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

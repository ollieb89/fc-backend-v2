# financial_dashboard/crypto_connectors/binance.py

import os
import requests
from urllib.parse import urlencode
from .base import BaseCryptoConnector

class BinanceConnector(BaseCryptoConnector):
    AUTH_BASE_URL = "https://www.binance.com/en/oauth/authorize"
    TOKEN_URL = "https://www.binance.com/en/oauth/token"
    API_BASE_URL = "https://api.binance.com"

    def __init__(self):
        # For the manual integration, these values are not used,
        # but they are required for the OAuth interface.
        self.client_id = os.getenv('BINANCE_CLIENT_ID', 'your_actual_client_id')
        self.client_secret = os.getenv('BINANCE_CLIENT_SECRET', 'your_actual_client_secret')
        self.redirect_uri = os.getenv('BINANCE_REDIRECT_URI', 'https://your-backend-domain.com/api/binance/callback/')

    def get_authorization_url(self, state=None):
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "read_user",
        }
        if state:
            params["state"] = state
        return f"{self.AUTH_BASE_URL}?{urlencode(params)}"

    def exchange_code_for_token(self, code):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        response = requests.post(self.TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()

    def get_user_data(self, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        # Example endpoint – adjust according to Binance API documentation.
        response = requests.get(f"{self.API_BASE_URL}/api/v3/account", headers=headers)
        response.raise_for_status()
        return response.json()

# financial_dashboard/crypto_connectors/base.py

from abc import ABC, abstractmethod

class BaseCryptoConnector(ABC):
    """
    Abstract base class for crypto exchange connectors.
    """

    @abstractmethod
    def get_authorization_url(self, state=None):
        """
        Return the URL to redirect the user for authorization.
        """
        pass

    @abstractmethod
    def exchange_code_for_token(self, code):
        """
        Exchange the provided code for an access token.
        """
        pass

    @abstractmethod
    def get_user_data(self, access_token):
        """
        Retrieve the user data using the given access token.
        """
        pass

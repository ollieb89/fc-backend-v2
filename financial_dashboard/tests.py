import datetime
from django.test import TestCase
from django.urls import reverse

# Import the new models from your financial_dashboard app.
from .models import User, FinancialInstitution, UserAccount, Category, Transaction

def create_test_data():
    """
    Helper function to create and return test data for our financial dashboard.
    """
    # Create a test user.
    user = User.objects.create(
        email="testuser@example.com",
        password_hash="fakehash123"
    )

    # Create a test financial institution.
    institution = FinancialInstitution.objects.create(
        name="Test Bank",
        institution_type="bank",
        country="US",
        base_url="https://testbank.com"
    )

    # Create a test user account.
    account = UserAccount.objects.create(
        user=user,
        institution=institution,
        account_name="Test Checking",
        official_name="Test Checking Account",
        account_type="checking",
        currency="USD",
        balance_current=1000.00
    )

    # Create a test category.
    category = Category.objects.create(
        name="Groceries",
        type="expense"
    )

    # Create a test transaction.
    transaction = Transaction.objects.create(
        account=account,
        user=user,
        amount=-50.00,
        currency="USD",
        date=datetime.datetime.now(),
        pending=False,
        description="Grocery shopping",
        transaction_type="debit"
    )

    return {
        "user": user,
        "institution": institution,
        "account": account,
        "category": category,
        "transaction": transaction
    }

class FinancialDashboardViewsTestCase(TestCase):
    def setUp(self):
        # Create test data for use in view tests.
        self.data = create_test_data()

    def test_index_page_loads(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        # Check that the page contains text that should be in your index template,
        # for example "Financial Dashboard" (adjust as needed).
        self.assertContains(response, "Financial Dashboard")

    def test_dashboard_page_loads(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        # Check that the dashboard template contains a known string.
        self.assertContains(response, "Dashboard")

class FinancialDashboardModelsTestCase(TestCase):
    def setUp(self):
        # Create test data for model tests.
        self.data = create_test_data()
        self.user = self.data["user"]
        self.category = self.data["category"]
        self.transaction = self.data["transaction"]

    def test_user_str(self):
        # The __str__ method for User returns the email.
        self.assertEqual(str(self.user), "testuser@example.com")

    def test_category_str(self):
        # The __str__ method for Category returns its name.
        self.assertEqual(str(self.category), "Groceries")

    def test_transaction_str(self):
        # The __str__ method for Transaction is defined as:
        #   return f"{self.description} ({self.amount})"
        expected_str = f"{self.transaction.description} ({self.transaction.amount})"
        self.assertEqual(str(self.transaction), expected_str)

    def test_transaction_creation(self):
        # Ensure that exactly one transaction exists.
        self.assertEqual(Transaction.objects.count(), 1)
        # Verify its details.
        self.assertEqual(self.transaction.description, "Grocery shopping")
        self.assertEqual(self.transaction.amount, -50.00)
        self.assertEqual(self.transaction.currency, "USD")

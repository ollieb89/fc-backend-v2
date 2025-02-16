# financial_dashboard/admin.py

from django.contrib import admin
from .models import (
    User, FinancialInstitution, UserAccount, Transaction, Category,
    Budget, InvestmentHolding, CryptoWallet, AIInsight, Notification,
    AuditLog, APIConnection, MLModel
)

admin.site.register(User)
admin.site.register(FinancialInstitution)
admin.site.register(UserAccount)
admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(InvestmentHolding)
admin.site.register(CryptoWallet)
admin.site.register(AIInsight)
admin.site.register(Notification)
admin.site.register(AuditLog)
admin.site.register(APIConnection)
admin.site.register(MLModel)

# fc_backend_v2/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('financial_dashboard.api_urls')),
    path('', include('financial_dashboard.urls')),
]

# fc_backend_v2/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from financial_dashboard.api_views import UserViewSet
from rest_framework.routers import DefaultRouter

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('financial_dashboard.api_urls')),  # Your existing API routes
    path('api/auth/', include(router.urls)),  # User-related endpoints (e.g., /api/auth/users/me/)

    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verify token

    # Frontend routes (if serving frontend from Django)
    path('', include('financial_dashboard.urls')),
]
"""
URL configuration for Secure Banking API Simulation.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App routes
    path('api/core/', include('core.urls')),
    path('api/banking/', include('banking.urls')),
    path('api/security/', include('security.urls')),
]

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.throttles import AuthRateThrottle


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [AuthRateThrottle]


class ThrottledTokenRefreshView(TokenRefreshView):
    throttle_classes = [AuthRateThrottle]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', ThrottledTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', ThrottledTokenRefreshView.as_view(), name='token_refresh'),
    path('api/core/', include('core.urls')),
    path('api/banking/', include('banking.urls')),
    path('api/security/', include('security.urls')),
]

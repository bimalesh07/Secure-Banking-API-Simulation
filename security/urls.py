from django.urls import path
from . import views

urlpatterns = [
    path('action-requests/', views.CreateActionRequestView.as_view(), name='create-action-request'),
    path('action-requests/pending/', views.PendingActionRequestsView.as_view(), name='pending-actions'),
    path('action-requests/all/', views.AllActionRequestsView.as_view(), name='all-actions'),
    path('action-requests/<int:pk>/review/', views.ReviewActionRequestView.as_view(), name='review-action'),
    path('otp/generate/', views.GenerateOTPView.as_view(), name='generate-otp'),
]

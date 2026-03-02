from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('create-staff/', views.CreateStaffView.as_view(), name='create-staff'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]

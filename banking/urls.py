from django.urls import path
from . import views

urlpatterns = [
    path('my-account/', views.MyAccountView.as_view(), name='my-account'),
    path('accounts/', views.AccountListView.as_view(), name='account-list'),
    path('lookup/', views.AccountLookupView.as_view(), name='account-lookup'),
    path('transfer/', views.TransferView.as_view(), name='transfer'),
    path('transactions/', views.TransactionHistoryView.as_view(), name='transaction-history'),
]

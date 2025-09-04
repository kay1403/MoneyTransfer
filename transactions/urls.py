from django.urls import path
from .views import TransactionCreateView, TransactionListView

urlpatterns = [
    path('create/', TransactionCreateView.as_view(), name='create-transaction'),
    path('', TransactionListView.as_view(), name='list-transactions'),
    path('receipt/<int:pk>/', TransactionReceiptView.as_view(), name='transaction-receipt'),
]

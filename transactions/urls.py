from django.urls import path
from .views import (
    TransactionCreateView,
    TransactionListView,
    TransactionConfirmView,
    TransactionReceiptView
)

urlpatterns = [
    path('create/', TransactionCreateView.as_view(), name='create-transaction'),
    path('', TransactionListView.as_view(), name='list-transactions'),
    path('confirm/<int:pk>/', TransactionConfirmView.as_view(), name='confirm-transaction'),  # confirmation
    path('receipt/<int:pk>/', TransactionReceiptView.as_view(), name='transaction-receipt'), # téléchargement PDF
]

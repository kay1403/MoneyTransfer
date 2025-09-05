from django.urls import path
from .views import TransactionCreateView, TransactionListView, TransactionConfirmView, TransactionReceiptView

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction-list'),  # GET
    path('create/', TransactionCreateView.as_view(), name='transaction-create'),  # POST
    path('<int:pk>/confirm/', TransactionConfirmView.as_view(), name='transaction-confirm'),
    path('receipt/<int:pk>/', TransactionReceiptView.as_view(), name='transaction-receipt'),
]

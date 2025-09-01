from django.urls import path
from .views import RegisterView, LoginView, TransactionCreateView, TransactionListView, NotificationListView, ConvertCurrencyView
from . import views

urlpatterns = [
    path('', views.api_index, name='core-index'),
    path('convert/', ConvertCurrencyView.as_view(), name='convert'),  # <-- updated to APIView
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('transactions/create/', TransactionCreateView.as_view(), name='create-transaction'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
]

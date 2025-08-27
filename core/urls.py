from django.urls import path
from .views import RegisterView, LoginView, TransactionCreateView, TransactionListView, NotificationListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('transactions/create/', TransactionCreateView.as_view(), name='create-transaction'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
]

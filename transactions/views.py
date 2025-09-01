from rest_framework import generics, permissions
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    parser_classes = (permissions.AllowAny,)  # Pour multipart/form-data
    permission_classes = [permissions.IsAuthenticated]

class TransactionListView(generics.ListCreateAPIView):  # <-- ListCreateAPIView au lieu de ListAPIView
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # Ajoutez permissions si nécessaire

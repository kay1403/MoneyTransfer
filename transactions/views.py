from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)

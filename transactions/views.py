from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Transaction
from .serializers import TransactionSerializer
from .utils import generate_receipt, send_transaction_notification

# --- Create transaction ---
class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    parser_classes=[MultiPartParser, FormParser]   
    permission_classes=[IsAuthenticated]
# --- List transactions for sender/receiver ---
class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)

# --- Confirm transaction (receiver) ---
class TransactionConfirmView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        transaction = self.get_object()
        user = request.user
        if transaction.receiver != user:
            return Response({"detail": "Unauthorized"}, status=403)
        
        transaction.status = 'CONFIRMED'
        transaction.save()

        # Notification en temps réel au sender
        send_transaction_notification(transaction)

        return Response({"detail": "Transaction confirmed"})

# --- Download PDF receipt ---
class TransactionReceiptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        user = request.user
        if transaction.sender != user and transaction.receiver != user:
            return Response({"detail": "Unauthorized"}, status=403)
        
        # Génère et retourne le PDF
        return generate_receipt(transaction)

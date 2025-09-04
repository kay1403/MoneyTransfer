from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Transaction
from .utils import generate_receipt

class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    parser_classes = [MultiPartParser, FormParser]  # nécessaire pour upload fichiers
    permission_classes = [permissions.IsAuthenticated]

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Retourne toutes les transactions où l'utilisateur est sender ou receiver
        return Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)

class TransactionConfirmView(generics.UpdateAPIView):
    """
    Permet au receiver de confirmer qu'il a envoyé le Mobile Money
    """
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

        # Ici, tu pourrais générer un PDF ou un reçu numérique
        from .utils import send_transaction_notification
        send_transaction_notification(transaction)

        return Response({"detail": "Transaction confirmed"})

class TransactionReceiptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        user = request.user
        if transaction.sender != user and transaction.receiver != user:
            return Response({"detail": "Unauthorized"}, status=403)
        return generate_receipt(transaction)

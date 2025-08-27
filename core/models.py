from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    amount_sender = models.DecimalField(max_digits=12, decimal_places=2)
    amount_receiver = models.DecimalField(max_digits=12, decimal_places=2)
    currency_sender = models.CharField(max_length=5)
    currency_receiver = models.CharField(max_length=5)
    status = models.CharField(max_length=20, default='pending')
    proof_url = models.URLField(blank=True, null=True)
    proof = models.ImageField(upload_to='proofs/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    message = models.TextField()
    read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

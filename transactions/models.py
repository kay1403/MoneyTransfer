from django.db import models
from accounts.models import User

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('FAILED', 'Failed'),
    )

    # ForeignKey avec related_name unique
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='transactions_sent'  # UNIQUE dans tout le projet
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='transactions_received'  # UNIQUE dans tout le projet
    )

    amount_sender = models.DecimalField(max_digits=12, decimal_places=2)
    amount_receiver = models.DecimalField(max_digits=12, decimal_places=2)
    currency_sender = models.CharField(max_length=5)
    currency_receiver = models.CharField(max_length=5)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    proof = models.ImageField(upload_to='proofs/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username} : {self.amount_receiver} {self.currency_receiver} ({self.status})"

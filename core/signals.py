from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Transaction, Notification

def send_transaction_notification(transaction: Transaction):
    # Créer notification en base
    notif = Notification.objects.create(
        user=transaction.receiver,
        transaction=transaction,
        message=f"Nouvelle transaction de {transaction.sender.username} : {transaction.amount_receiver} {transaction.currency_receiver}"
    )

    # Envoyer notification via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{transaction.receiver.id}",
        {
            "type": "send_notification",
            "message": notif.message
        }
    )

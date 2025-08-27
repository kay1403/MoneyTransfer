import requests
from PIL import Image
import pytesseract
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def get_exchange_rate(from_currency: str, to_currency: str):
    API_KEY = 'VOTRE_API_KEY_EXCHANGE'
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}'
    try:
        res = requests.get(url).json()
        return res['conversion_rates'].get(to_currency)
    except:
        return None

def verify_proof(proof_path, amount_expected):
    try:
        img = Image.open(proof_path)
        text = pytesseract.image_to_string(img)
        return str(amount_expected) in text
    except:
        return False


def send_transaction_notification(transaction):
    """
    Envoie notification au receiver via WebSocket
    """
    channel_layer = get_channel_layer()
    message = f"Nouvelle transaction de {transaction.sender.username} : {transaction.amount_receiver} {transaction.currency_receiver}"
    async_to_sync(channel_layer.group_send)(
        f"user_{transaction.receiver.id}",
        {
            "type": "send_notification",
            "message": message
        }
    )

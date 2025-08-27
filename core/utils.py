import requests
from decouple import config  # pour sécuriser la clé API

API_KEY = config('OPEN_EXCHANGE_API_KEY')  # mettre la clé dans .env

def get_exchange_rate(from_currency: str, to_currency: str):
    url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}&base={from_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        rate = data.get('rates', {}).get(to_currency)
        if rate:
            return rate
        else:
            raise ValueError(f"Taux pour {to_currency} non trouvé.")
    except Exception as e:
        print(f"Erreur récupération taux: {e}")
        return None

import pytesseract
from PIL import Image

def verify_proof(proof_path, amount_expected):
    """
    Vérifie automatiquement le reçu via OCR
    """
    try:
        img = Image.open(proof_path)
        text = pytesseract.image_to_string(img)

        # Cherche le montant exact dans le texte
        amount_str = str(amount_expected)
        if amount_str in text:
            return True
        return False
    except Exception as e:
        print(f"Erreur OCR: {e}")
        return False

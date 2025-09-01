from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Transaction, Notification
from .serializers import UserSerializer, TransactionSerializer, NotificationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from decimal import Decimal, InvalidOperation
from rest_framework_simplejwt.authentication import JWTAuthentication


# Inscription
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Login (JWT)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=400)

# Créer une transaction
class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    parser_classes = (MultiPartParser, FormParser)

# Liste des transactions de l'utilisateur
class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)

# Notifications
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user).order_by('-created_at')

def api_index(request):
    """
    Simple JSON index for /api/core/ — évite le 404 quand on redirige /api/ -> /api/core/
    """
    return JsonResponse({
        "name": "MoneyTransfer Core API",
        "endpoints": {
            "convert": "/api/core/convert/",
            "register": "/api/core/register/",
            "login": "/api/core/login/",
            "transactions": "/api/core/transactions/",
            "notifications": "/api/core/notifications/",
        }
    })

class ConvertCurrencyView(APIView):
    """
    Conversion using exchangerate.host with a static fallback.
    Uses DRF APIView so CSRF is not required for JSON POSTs.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({
            "detail": "POST {from_currency, to_currency, amount} to convert",
            "example": {"from_currency": "XAF", "to_currency": "RWF", "amount": 100}
        })

    def post(self, request, *args, **kwargs):
        payload = request.data or {}
        from_currency = (payload.get("from_currency") or "").upper()
        to_currency = (payload.get("to_currency") or "").upper()
        amount = payload.get("amount")

        if not from_currency or not to_currency or amount is None:
            return Response({"detail": "Missing from_currency, to_currency or amount"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amt = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            return Response({"detail": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

        # Try exchangerate.host first
        try:
            resp = requests.get(
                "https://api.exchangerate.host/convert",
                params={"from": from_currency, "to": to_currency, "amount": str(amt)},
                timeout=5
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("success") is True and "result" in data:
                info = data.get("info") or {}
                rate = None
                if info.get("rate"):
                    rate = Decimal(str(info.get("rate")))
                else:
                    # derive rate if needed
                    try:
                        rate = (Decimal(str(data["result"])) / amt).quantize(Decimal("0.0000001"))
                    except Exception:
                        rate = None

                converted = Decimal(str(data["result"])).quantize(Decimal("0.01"))
                return Response({
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "amount": str(amt),
                    "rate": str(rate) if rate is not None else None,
                    "converted_amount": str(converted),
                    "source": "exchangerate.host",
                })
        except requests.RequestException:
            # external API failed; fall through to fallback
            pass
        except (ValueError, KeyError):
            pass

        # Static fallback rates
        EXAMPLE_RATES = {
            ("XAF", "RWF"): Decimal("1.50"),
            ("RWF", "XAF"): Decimal("0.66"),
            ("USD", "EUR"): Decimal("0.92"),
            ("EUR", "USD"): Decimal("1.09"),
            ("USD", "XAF"): Decimal("600.00"),
            ("XAF", "USD"): Decimal("0.0017"),
        }

        if from_currency == to_currency:
            rate = Decimal("1")
        else:
            rate = EXAMPLE_RATES.get((from_currency, to_currency))

        if rate is None:
            return Response({"error": "Impossible de récupérer le taux de change."}, status=status.HTTP_502_BAD_GATEWAY)

        converted = (amt * rate).quantize(Decimal("0.01"))
        return Response({
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": str(amt),
            "rate": str(rate),
            "converted_amount": str(converted),
            "source": "fallback",
        })


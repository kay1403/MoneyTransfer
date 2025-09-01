from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.utils import timezone

User = get_user_model()
signer = TimestampSigner()

# Endpoint d'inscription
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

# Optionnel : liste tous les users (admin uniquement)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """
    POST JSON { "username": "...", "password": "..." }
    Returns { "access": "<signed token>" } on success (frontend expects an access token).
    """
    try:
        payload = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        return HttpResponseBadRequest("Missing username or password")

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"detail": "Invalid credentials"}, status=401)

    # Create a simple signed token (TimestampSigner) — expires can be enforced when validating
    data = {"user_id": user.id, "iat": timezone.now().timestamp()}
    token_payload = json.dumps(data)
    token = signer.sign(token_payload)

    return JsonResponse({"access": token})

@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    """
    POST JSON { "username": "...", "password": "...", "email": "..." }
    Creates a Django user and returns basic info.
    """
    try:
        payload = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    username = payload.get("username")
    password = payload.get("password")
    email = payload.get("email", "")

    if not username or not password:
        return HttpResponseBadRequest("Missing username or password")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"detail": "Username already taken"}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    return JsonResponse({"id": user.id, "username": user.username}, status=201)

# Helper to validate token elsewhere (example)
def validate_signed_token(token, max_age=None):
    """
    Return dict payload if token valid, otherwise raise BadSignature/SignatureExpired.
    max_age in seconds (optional).
    """
    try:
        raw = signer.unsign(token, max_age=max_age)
        return json.loads(raw)
    except (BadSignature, SignatureExpired):
        raise

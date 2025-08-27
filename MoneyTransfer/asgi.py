import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import transactions.routing  # changer ici

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MoneyTransfer.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            transactions.routing.websocket_urlpatterns  # utiliser routing de transactions
        )
    ),
})

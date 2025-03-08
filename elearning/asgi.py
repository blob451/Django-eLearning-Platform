import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # Ensure this file exists in chat app
import notifications.routing  # Optional: if you have notifications app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns + notifications.routing.websocket_urlpatterns
        )
    ),
})

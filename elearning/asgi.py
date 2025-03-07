"""
ASGI config for elearning project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
<<<<<<< HEAD

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')

application = get_asgi_application()
=======
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # if you created a chat app with routing; adjust as needed

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # adjust if your routing is in a different module
        )
    ),
})
>>>>>>> d91aa4e (2 - Basic app configurations and models)

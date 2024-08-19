"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.urls import path
from django.urls import re_path
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from blog_api.consumers import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_asgi_application()

ws_patterns = [
    path(
        'ws/notification/<int:user_id>/<str:token>/', NotificationConsumer.as_asgi())
]
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(ws_patterns)
})

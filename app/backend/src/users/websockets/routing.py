from django.urls import re_path

from users.websockets.consumers import UserConsumer


websocket_urlpatterns = [
    re_path(r'^ws/$', UserConsumer.as_asgi()),
]

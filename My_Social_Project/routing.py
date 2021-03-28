from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from App_chat.consumers import EchoConsumer, ChatConsumer
from channels.auth import AuthMiddlewareStack
from App_chat.token_auth import TokenAuthMiddleware

application = ProtocolTypeRouter({
    'websocket' : TokenAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/chat/<str:username>/',ChatConsumer),
                path('ws/chat/', EchoConsumer)
            ])
        ),
    )
    
})
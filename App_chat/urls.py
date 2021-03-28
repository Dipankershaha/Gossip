from django.urls import path, include
from App_chat.views import ThreadView

app_name = "App_chat"

urlpatterns = [
    path('<str:username>/', ThreadView.as_view(),name='chat')
]


from django.urls import path
from . import views

urlpatterns = [
    path("start/", views.start_chat, name="chat-start"),
    path("<uuid:conversation_id>/messages/", views.chat_messages, name="chat-messages"),
    path("staff/conversations/", views.staff_conversations, name="staff-conversations"),
    path("staff/<uuid:conversation_id>/reply/", views.staff_reply, name="staff-reply"),
]

from uuid import UUID
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def start_chat(request):
    subject = str(request.data.get("subject", "Customer support")).strip()[:160] or "Customer support"
    guest_name = str(request.data.get("name", "")).strip()[:100]
    guest_email = str(request.data.get("email", "")).strip()[:254]
    conversation = Conversation.objects.create(
        customer=request.user if request.user.is_authenticated else None,
        guest_name=guest_name, guest_email=guest_email, subject=subject,
    )
    first_message = str(request.data.get("message", "")).strip()[:3000]
    if first_message:
        Message.objects.create(
            conversation=conversation,
            sender=request.user if request.user.is_authenticated else None,
            sender_label=(request.user.get_username() if request.user.is_authenticated else guest_name or "Guest"),
            body=first_message,
        )
    return Response({"conversation_id": str(conversation.id), "status": conversation.status}, status=status.HTTP_201_CREATED)

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def chat_messages(request, conversation_id):
    try:
        UUID(str(conversation_id))
    except (ValueError, TypeError):
        return Response({"detail": "Invalid conversation ID."}, status=status.HTTP_400_BAD_REQUEST)
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    if request.method == "GET":
        after_id = request.query_params.get("after", "0")
        try:
            after_id = max(0, int(after_id))
        except ValueError:
            after_id = 0
        messages = conversation.messages.filter(id__gt=after_id)[:200]
        return Response({"status": conversation.status, "messages": MessageSerializer(messages, many=True).data})
    if conversation.status == Conversation.Status.CLOSED:
        return Response({"detail": "This chat is closed."}, status=status.HTTP_400_BAD_REQUEST)
    body = str(request.data.get("body", "")).strip()
    if not body:
        return Response({"detail": "Message cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
    if len(body) > 3000:
        return Response({"detail": "Message is too long."}, status=status.HTTP_400_BAD_REQUEST)
    label = request.user.get_username() if request.user.is_authenticated else (conversation.guest_name or "Guest")
    message = Message.objects.create(conversation=conversation, sender=request.user if request.user.is_authenticated else None, sender_label=label, body=body)
    conversation.save(update_fields=["updated_at"])
    return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAdminUser])
def staff_conversations(request):
    qs = Conversation.objects.select_related("customer", "assigned_to").prefetch_related("messages")[:200]
    return Response([{
        "id": str(c.id), "subject": c.subject, "status": c.status,
        "customer": c.customer.username if c.customer else c.guest_name or "Guest",
        "email": c.guest_email, "updated_at": c.updated_at,
        "messages": MessageSerializer(c.messages.all(), many=True).data,
    } for c in qs])

@api_view(["POST"])
@permission_classes([IsAdminUser])
def staff_reply(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    body = str(request.data.get("body", "")).strip()
    if not body or len(body) > 3000:
        return Response({"detail": "Reply must be between 1 and 3000 characters."}, status=status.HTTP_400_BAD_REQUEST)
    message = Message.objects.create(conversation=conversation, sender=request.user, sender_label="NOVAMART Support", body=body, is_staff_reply=True)
    conversation.status = Conversation.Status.WAITING
    conversation.assigned_to = request.user
    conversation.save(update_fields=["status", "assigned_to", "updated_at"])
    return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

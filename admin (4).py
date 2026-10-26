from django.contrib import admin
from .models import Conversation, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("sender", "sender_label", "body", "is_staff_reply", "created_at")

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "customer", "guest_name", "status", "assigned_to", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "subject", "guest_name", "guest_email", "customer__username")
    readonly_fields = ("id", "created_at", "updated_at")
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender_label", "is_staff_reply", "created_at")
    list_filter = ("is_staff_reply", "created_at")
    search_fields = ("body", "sender_label")

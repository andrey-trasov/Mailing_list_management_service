from django.contrib import admin
from mailings.models import Client, Message, Newsletter, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "fio", "comment")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("name", "start_time", "end_time", "time_last_shipment", "periodicity", "status", "message")

@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ("name", "mailing", "attempt_time", "attempt", "comments", "response")

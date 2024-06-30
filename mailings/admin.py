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
    list_display = ("start_time", "end_time", "periodicity", "status")

@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ("attempt_time", "attempt", "response")

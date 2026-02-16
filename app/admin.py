from django.contrib import admin
from .models import Email

@admin.register(Email)
class SentEmailAdmin(admin.ModelAdmin):
    list_display = ('to_email', 'subject', 'sent_at')
    search_fields = ('to_email', 'subject')
    date_hierarchy = 'sent_at'
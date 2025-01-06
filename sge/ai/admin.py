from django.contrib import admin
from .models import AIResult


@admin.register(AIResult)
class AIResultAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'result')

from django.contrib import admin
from .models import Suggestion

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'text_excerpt', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'text')

    def text_excerpt(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_excerpt.short_description = 'Feedback Text'

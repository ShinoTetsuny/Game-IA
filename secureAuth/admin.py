from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_usage_count')
    search_fields = ('user__username', 'user__email')
    list_filter = ('api_usage_count',)

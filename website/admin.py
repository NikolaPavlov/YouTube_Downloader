from .models import Statistics
from django.contrib import admin


# Register your models here.
@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('ip', 'daily_downloads', 'time_of_last_dl')
    ordering = ('-time_of_last_dl',)

from django.contrib import admin

# Register your models here.

from .models import Speed


class SpeedAdmin(admin.ModelAdmin):
    list_display = ('speed_time', 'speed_value')

admin.site.register(Speed, SpeedAdmin)

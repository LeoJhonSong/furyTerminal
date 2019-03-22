from django.contrib import admin

# Register your models here.

from .models import Speed


class SpeedAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is not None, so this is an edit
            return ['speed_value']  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []

    list_display = ('speed_time', 'speed_value')

admin.site.register(Speed, SpeedAdmin)

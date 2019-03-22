from django.db import models

# Create your models here.


class Speed(models.Model):
    speed_value = models.CharField(max_length=50)
    speed_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'time: ' + str(self.speed_time)


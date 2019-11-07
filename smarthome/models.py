from django.db import models

class Scheduler(models.Model):
    device = models.CharField('Device', max_length=120)
    status = models.IntegerField('Status')
    event = models.CharField('Event',max_length=120)
    time = models.CharField('Time',max_length = 60)
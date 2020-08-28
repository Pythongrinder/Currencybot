from django.db import models

class Notifications(models.Model):
    Link = models.CharField(max_length=200)
    BiggerThan = models.FloatField(default=0)
    SmallerThan = models.FloatField(default=0)

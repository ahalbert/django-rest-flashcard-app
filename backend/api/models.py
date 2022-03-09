from django.db import models
from datetime import datetime 
from django.utils import timezone

# Create your models here.
class Card(models.Model):
    word = models.CharField(max_length=50) 
    definition  = models.CharField(max_length=500) 
    bucket = models.IntegerField(default=0)
    dateNextReviewed = models.DateTimeField(default=timezone.now)
    numberOfTimesWrong = models.IntegerField(default=0)

    def __str__(self):
        return self.word + ":" + self.definition 

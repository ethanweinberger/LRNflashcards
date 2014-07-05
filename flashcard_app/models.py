from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class FlashcardGroup(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    front_side = models.CharField(max_length=50)
    back_side = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
    
class Flashcard(models.Model):
    frontside = models.CharField(max_length=50)
    backside = models.CharField(max_length=50)
    active = models.BooleanField(default = True)
    times_wrong = models.IntegerField(default = 0)
    times_to_repeat = models.IntegerField(default = 0)
    group = models.ForeignKey(FlashcardGroup)
    
    def __unicode__(self):
        return self.frontside + " / " + self.backside
    
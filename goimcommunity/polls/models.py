from django.db import models

import datetime

# Create your models here.

class Poll(models.Model):
    question = models.CharField(maxlength=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question

    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()

    class Admin:
        pass

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(maxlength=200)
    votes = models.IntegerField()

    def __str__(self):
        return self.choice

    class Admin:
        pass

    



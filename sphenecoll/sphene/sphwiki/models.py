from django.db import models

from django.contrib.auth.models import User

from sphene.community.models import Group

from datetime import datetime


class WikiSnip(models.Model):
    name = models.CharField(maxlength = 250)
    group = models.ForeignKey(Group)
    body = models.TextField()
    creator = models.ForeignKey(User, related_name = 'wikisnip_created', editable = True)
    created = models.DateTimeField(editable = False)
    editor  = models.ForeignKey(User, related_name = 'wikisnip_edited', editable = True)
    changed = models.DateTimeField(editable = False)

    def save(self):
        if not self.id:
            self.created = datetime.today()
        self.changed = datetime.today()
        super(WikiSnip, self).save()

    def __str__(self):
        return self.name

    class Admin:
        pass

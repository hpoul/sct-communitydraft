from django.db import models
from django.contrib.auth.models import User

from sphene.community.models import Group

# Create your models here.

class Project(models.Model):
    group = models.OneToOneField(Group)
    owner = models.ForeignKey(User)

    def recursiveName(self):
        return self.group.recursiveName()

    recursiveName.short_description = 'Project'

    def __str__(self):
        return self.recursiveName();

    class Admin:
        list_display = ('recursiveName', 'owner')
        list_filter = ['owner']
        pass

class Task(models.Model):
    project = models.ForeignKey(Project)
    title = models.CharField(maxlength = 250)
    author = models.ForeignKey(User, related_name = 'task_author')
    owner = models.ForeignKey(User, related_name = 'task_owner')
    postdate = models.DateTimeField( auto_now_add = True )
    description = models.TextField(blank = True)

    def __str__(self):
        return self.title;

    class Admin:
        list_filter = ['project', 'owner']
        list_display = ('title', 'project', 'owner' )
        pass


class TimeEntry(models.Model):
    owner = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    postdate = models.DateTimeField(auto_now_add = True)
    description = models.TextField(blank = True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def project(self):
        return self.task.project.recursiveName()
    project.short_description = 'Project'

    def duration(self):
        return self.end - self.start
    duration.short_description = 'Duration'

    def __str__(self):
        return self.description;

    class Meta:
        ordering = [ '-start' ]

    class Admin:
    	list_filter = ['task','owner']
	list_display = ('task', 'owner', 'project', 'description', 'duration', 'start', 'end')
        pass

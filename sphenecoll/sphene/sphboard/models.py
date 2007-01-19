from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from sphene.community.models import Group

POSTS_ALLOWED_CHOICES = (
    (-1, 'All Users'),
    (0, 'Loggedin Users'),
    (1, 'Members of the Group'),
    (2, 'Administrators'),
    (3, 'Nobody'),
    )

# Create your models here.
class Category(models.Model):
    name = models.CharField(maxlength = 250)
    group = models.ForeignKey(Group, null = True, blank = True)
    parent = models.ForeignKey('self', related_name = 'childs', null = True, blank = True)
    description = models.TextField(blank = True)
    allowthreads = models.IntegerField( default = 0, choices = POSTS_ALLOWED_CHOICES )
    allowreplies = models.IntegerField( default = 0, choices = POSTS_ALLOWED_CHOICES )

    def canContainPosts(self):
        return self.allowthreads != 3

    def thread_list(self):
        return self.posts.filter( thread__isnull = True )

    def threadCount(self):
        return self.posts.filter( thread__isnull = True ).count()

    def postCount(self):
        return self.posts.count()

    def latestPost(self):
        return self.posts.latest( 'postdate' )

    def allowPostThread(self, user):
        return self.testAllowance(user, self.allowthreads)

    def testAllowance(self, user, level):
        if level == -1:
            return True;
        if user == None:
            return False;
        if level == 0:
            return True;
        return False;

    def __str__(self):
        return self.name;
    
    class Admin:
        search_fields = ('name')

class Post(models.Model):
    category = models.ForeignKey(Category, related_name = 'posts')
    subject = models.CharField(maxlength = 250)
    body = models.TextField()
    thread = models.ForeignKey('self', null = True)
    postdate = models.DateTimeField( auto_now_add = True )
    author = models.ForeignKey(User)

    def get_thread(self):
        if self.thread == None: return self;
        return self.thread;

    def latestPost(self):
        return self.allPosts().latest( 'postdate' )

    def allPosts(self):
        return Post.objects.filter( Q( pk = self.id ) | Q( thread = self ) )

    def postCount(self):
        return self.allPosts().count()

    def allowPosting(self, user):
        return self.category.testAllowance( user, self.category.allowreplies )

    def __str__(self):
        return self.subject

    class Admin:
        pass

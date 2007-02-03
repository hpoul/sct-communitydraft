from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from sphene.community.models import Group

from django.utils import html
from text import bbcode

import re

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
        if user == None or not user.is_authenticated():
            return False;
        if level == 0:
            return True;
        return False;

    def __str__(self):
        return self.name;
    
    class Admin:
        search_fields = ('name')

ALLOWED_TAGS = {
    'p': ( 'align' ),
    'em': (),
    'strike': (),
    'strong': (),
    'img': ( 'src', 'width', 'height', 'border', 'alt', 'title' ),
    'u': ( ),
    }

#USED_STYLE = 'html'
USED_STYLE = 'bbcode'

def htmlentities_replace(test):
    print "entity allowed: %s" % test.group(1)
    return test.group()

def htmltag_replace(test):
    if ALLOWED_TAGS.has_key( test.group(2) ):
        print "tag is allowed.... %s - %s" % (test.group(), test.group(3))
        if test.group(3) == None: return test.group()
        attrs = test.group(3).split(' ')
        allowedParams = ALLOWED_TAGS[test.group(2)]
        i = 1
        allowed = True
        for attr in attrs:
            if attr == '': continue
            val = attr.split('=')
            if not val[0] in allowedParams:
                allowed = False
                print "Not allowed: %s" % val[0]
                break
        if allowed: return test.group()
    print "tag is not allowed ? %s" % test.group(2)
    return test.group().replace('<','&lt;').replace('>','&gt;')

def bbcode_replace(test):
    print "bbcode ... %s %s %s" % (test.group(1), test.group(2), test.group(3))
    return test.group()

    
class Post(models.Model):
    category = models.ForeignKey(Category, related_name = 'posts', editable = False )
    subject = models.CharField(maxlength = 250)
    body = models.TextField()
    thread = models.ForeignKey('self', null = True, editable = False )
    postdate = models.DateTimeField( auto_now_add = True, editable = False )
    author = models.ForeignKey(User, editable = False )

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


    def body_escaped(self):
        body = self.body
        if USED_STYLE == 'html':
            regex = re.compile("&(?!nbsp;)");
            body = regex.sub( "&amp;", body )
            regex = re.compile("<(/?)([a-zA-Z]+?)( .*?)?/?>")
            return regex.sub( htmltag_replace, body )
        else:
            """
            body = html.escape( body )
            body = html.linebreaks( body )
            regex = re.compile("\[(.*?)\](?:([^\[]+)\[/(.*?)\])?")
            bbcode = regex.sub( bbcode_replace, body )
            """
            return bbcode.bb2xhtml(body)

    def __str__(self):
        return self.subject

    class Admin:
        pass

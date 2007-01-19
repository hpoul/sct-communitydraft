from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from sphene.community.models import Group

class GroupMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'groupName' in view_kwargs:
            print "we got a groupName: " +  view_kwargs['groupName']
            group = get_object_or_404(Group, name = view_kwargs['groupName'] )
            settings.TEMPLATE_DIRS = ( "/tmp/hehe", ) + settings.TEMPLATE_DIRS
        print " processing view ... "
        return None


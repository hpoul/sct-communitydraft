from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from sphene.community.models import Group

class GroupMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'urlPrefix' in view_kwargs:
            urlPrefix = view_kwargs['urlPrefix']
            if urlPrefix != '':
                urlPrefix = '/' + urlPrefix
            request.attributes['urlPrefix'] = urlPrefix
            del view_kwargs['urlPrefix']
        if 'groupName' in view_kwargs:
            group = get_object_or_404(Group, name = view_kwargs['groupName'] )
            del view_kwargs['groupName']
            view_kwargs['group'] = group
            request.attributes['group'] = group
            #settings.TEMPLATE_DIRS = ( "/tmp/hehe", ) + settings.TEMPLATE_DIRS
        return None



from django.conf import settings
from django.conf.urls.defaults import *

defaultdict = { 'groupName': None, #'SpaceCombat2',
                'urlPrefix': '', }

urlpatterns = patterns('',
                       (r'^$', 'django.views.generic.simple.redirect_to', { 'url': '/wiki/show/Start/' }),
                       (r'^board/', include('sphene.sphboard.urls'), defaultdict),
                       (r'^wiki/',  include('sphene.sphwiki.urls'), defaultdict),
                       (r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       (r'^accounts/logout/$', 'django.contrib.auth.views.logout' ),
		       (r'^accounts/register/$', 'sphene.community.views.register', defaultdict),
                       (r'^accounts/register/(?P<emailHash>[a-zA-Z/\+0-9=]+)/$', 'sphene.community.views.register_hash', defaultdict),

                       ## for development only ...
		       (r'^static/sphene/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/../../communitytools/static/sphene' }),
		       (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/../static' }),
                       )

from django.conf.urls.defaults import *
from wiki.feeds import *

from django.conf.urls.defaults import *


urlpatterns = patterns('',
                       (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'show/0/'}),
                       )
urlpatterns += patterns('sphene.sphboard.views',
                        (r'^show/(?P<category_id>\d+)/$', 'showCategory'),
                        (r'^thread/(?P<thread_id>\d+)/$', 'showThread'),
                        (r'^post/$', 'post'),
                       )




from django.conf.urls.defaults import *


urlpatterns = patterns('',
                       (r'^board/', include('sphene.sphboard.urls'), {'groupName': 'SpaceCombat2',
                                                                      'urlPrefix': '' }),
                       (r'^wiki/',  include('sphene.sphwiki.urls'), {'groupName': 'SpaceCombat2',
                                                                     'urlPrefix': '' }),
                       (r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       (r'^accounts/logout/$', 'django.contrib.auth.views.logout' ),
                       )

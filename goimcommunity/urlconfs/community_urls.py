
from django.conf import settings
from django.conf.urls.defaults import *
from sphene.sphwiki.sitemaps import WikiSnipSitemap
from sphene.sphboard.sitemaps import ThreadsSitemap
from sphene.sphwiki.feeds import LatestWikiChanges

defaultdict = { 'groupName': None,
                'urlPrefix': '', }

sitemaps = {
    'wiki': WikiSnipSitemap,
    'board': ThreadsSitemap,
    }

feeds = {
    'wiki': LatestWikiChanges,
    }

urlpatterns = patterns('',
                       (r'^$', 'django.views.generic.simple.redirect_to', { 'url': '/wiki/show/Start/' }),
                       (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', { 'sitemaps': sitemaps }),
                       (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
                       (r'^community/', include('sphene.community.urls'), { }),
                       (r'^board/', include('sphene.sphboard.urls'), defaultdict),
                       (r'^wiki/',  include('sphene.sphwiki.urls'), defaultdict),
                       (r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       (r'^accounts/logout/$', 'django.contrib.auth.views.logout' ),
		       (r'^accounts/register/$', 'sphene.community.views.register', defaultdict),
                       (r'^accounts/register/(?P<emailHash>[a-zA-Z/\+0-9=]+)/$', 'sphene.community.views.register_hash', defaultdict),

                       (r'^admin/', include('django.contrib.admin.urls')),
                       ## for development only ...
		       (r'^static/sphene/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/../../communitytools/static/sphene' }),
		       (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/../static' }),
                       )

from django.conf import settings
from django.urls import re_path, include, path

from sphene.community.sphutils import mediafiles_urlpatterns
from sphene.community.views import groupaware_redirect_to
from sphene.sphwiki.sitemaps import WikiSnipSitemap
from sphene.sphboard.sitemaps import ThreadsSitemap
from sphene.sphwiki.feeds import LatestWikiChanges

from django.views import static as views_static

defaultdict = { 'groupName': None,
                'urlPrefix': '', }

sitemaps = {
    'wiki': WikiSnipSitemap,
    'board': ThreadsSitemap,
    }

feeds = {
    'wiki': LatestWikiChanges,
    }

# newforms admin magic

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
                       #(r'^$', 'django.views.generic.simple.redirect_to', { 'url': '/wiki/show/Start/' }),
    re_path(r'^$', groupaware_redirect_to, { 'url': '/wiki/show/Start/', 'groupName': None }),
    #FIXME add sitemap
    # re_path(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', { 'sitemaps': sitemaps }),
    re_path(r'^feeds/(?P<url>.*)/$', LatestWikiChanges(), {'feed_dict': feeds}),
    re_path(r'^community/', include('sphene.community.urls'), defaultdict),
    re_path(r'^board/', include('sphene.sphboard.urls'), defaultdict),
    re_path(r'^wiki/',  include('sphene.sphwiki.urls'), defaultdict),
    re_path(r'^blog/',  include('sphene.sphblog.urls'), defaultdict),
                       #(r'^block/', include('sphene.sphblockframework.urls'), defaultdict),
    re_path(r'^questions/', include('sphene.sphquestions.urls'), defaultdict),
    path('accounts/', include('django.contrib.auth.urls')),

                       #(r'^accounts/register/$', 'sphene.community.views.register', defaultdict),
                       #(r'^accounts/register/(?P<emailHash>[a-zA-Z/\+0-9=]+)/$', 'sphene.community.views.register_hash', defaultdict),

    path('admin/', admin.site.urls),
                       ## for development only ...
    # re_path(r'^static/sphene/(.*)$', views_static.serve, {'document_root': settings.ROOT_PATH + '/../../communitytools/static/sphene' }),
    # re_path(r'^static/(?P<path>.*)$', views_static.serve, {'document_root': settings.ROOT_PATH + '/../static' }),

    path('i18n/', include('django.conf.urls.i18n')),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns() + mediafiles_urlpatterns()

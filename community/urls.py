from django.conf.urls import *
#from wiki.feeds import *
from django.conf import settings

# feeds for wikiPages and wikiNews
from django.conf.urls.static import static
from django.urls import re_path, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from sphene.community import views as community_views

"""
feeds = {
    'latestpages': LatestPages,
}

sitemaps = {
    'wiki': Wiki,
}
"""

# newforms admin magic

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    # Example:
    # (r'^goimcommunity/', include('goimcommunity.apps.foo.urls.foo')),

    # Uncomment this for admin:
    path(r'^admin/', admin.site.urls),

    re_path(r'^board/', include('sphene.sphboard.urls')),

    re_path(r'^(?P<urlPrefix>test/(?P<groupName>\w+))/board/', include('sphene.sphboard.urls')),
    re_path(r'^(?P<urlPrefix>test/(?P<groupName>\w+))/wiki/',  include('sphene.sphwiki.urls')),

    re_path(r'^wiki/',  include('sphene.sphwiki.urls'), { 'urlPrefix': 'wiki', 'groupName': 'Sphene' }),


    # re_path(r'^static/sphene/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/../../communitytools/static/sphene' }),
    # re_path(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/../static' }),



    #re_path(r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': '/home/kahless/dev/python/diamanda/media'}), # change it or remove if not on dev server

    # re_path(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    # re_path(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^accounts/register/(?P<emailHash>[a-zA-Z/\+0-9=]+)/$', community_views.register_hash),
                       

#                       (r'^forum/', include('myghtyboard.URLconf')), # forum
#                       (r'^muh/', 'wiki.views.show_page'), # wiki main page under /
#                       (r'^wiki/', include('wiki.URLconf')), # wiki
#                       (r'^wiki/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}), # wiki feeds
#                       (r'^wiki/sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}), # wikiPages sitemap


                       
]

#              + static(settings.STATIC_URL + 'sphene/', document_root=settings.ROOT_PATH + '/../../communitytools/static/sphene')
#              + static(settings.STATIC_URL, document_root=settings.ROOT_PATH + '/../static')

urlpatterns += staticfiles_urlpatterns()

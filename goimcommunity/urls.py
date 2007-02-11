from django.conf.urls.defaults import *
#from wiki.feeds import *
from django.conf import settings

from django.conf.urls.defaults import *
# feeds for wikiPages and wikiNews
"""
feeds = {
    'latestpages': LatestPages,
}

sitemaps = {
	'wiki': Wiki,
	}
"""
urlpatterns = patterns('',
    # Example:
    # (r'^goimcommunity/', include('goimcommunity.apps.foo.urls.foo')),

    # Uncomment this for admin:
                       (r'^admin/', include('django.contrib.admin.urls')),

                       (r'^polls/', include('goimcommunity.polls.urls')),
		       (r'^league/', include('goimcommunity.leaguesystem.urls')),

                       (r'^board/', include('sphene.sphboard.urls')),
                       (r'^rewrite/(?P<groupName>\w+)/board/', include('sphene.sphboard.urls'), {'urlPrefix': '' }),
                       (r'^rewrite/(?P<groupName>\w+)/wiki/',  include('sphene.sphwiki.urls'), {'urlPrefix': '' }),
		       (r'^rewrite/\w+/accounts/login/$', 'django.contrib.auth.views.login'),
		       (r'^rewrite/\w+/accounts/logout/$', 'django.contrib.auth.views.logout' ),
                       (r'^(?P<urlPrefix>test/(?P<groupName>\w+))/board/', include('sphene.sphboard.urls')),
                       (r'^(?P<urlPrefix>test/(?P<groupName>\w+))/wiki/',  include('sphene.sphwiki.urls')),

                       (r'^wiki/',  include('sphene.sphwiki.urls'), { 'urlPrefix': 'wiki', 'groupName': 'Sphene' }),


		       (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/../static' }),



                       (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': '/home/kahless/dev/python/diamanda/media'}), # change it or remove if not on dev server

                       (r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       (r'^accounts/logout/$','django.contrib.auth.views.logout'),
                       (r'^accounts/register/$', 'sphene.community.views.register' ),
                       

#                       (r'^forum/', include('myghtyboard.URLconf')), # forum
#                       (r'^muh/', 'wiki.views.show_page'), # wiki main page under /
#                       (r'^wiki/', include('wiki.URLconf')), # wiki
#                       (r'^wiki/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}), # wiki feeds
#                       (r'^wiki/sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}), # wikiPages sitemap


                       
)

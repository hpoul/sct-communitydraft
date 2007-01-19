from django.conf.urls.defaults import *
from goimcommunity.polls.models import Choice

info_dict = {
    'queryset': Choice.objects.all(),
    }

urlpatterns = patterns('',
                       (r'^$', 'django.views.generic.simple.direct_to_template', { 'template': 'leagueindex.html' }),
#                       (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
#                       (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
#                       (r'^(?P<object_id>\d+)/results/$','django.views.generic.list_detail.object_detail', dict(info_dict, template_name='polls/results.html')),
#                       (r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)
#urlpatterns = patterns('goimcommunity.polls.views',
#                       (r'^$', 'index'),
#                       (r'^(?P<poll_id>\d+)/$', 'detail'),
#                       (r'^(?P<poll_id>\d+)/results/$','results'),
#                       (r'^(?P<poll_id>\d+)/vote/$', 'vote'),
#)

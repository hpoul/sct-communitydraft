from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext


from sphene.sphwiki.models import WikiSnip


# Create your views here.


def showSnip(request, groupName, snipName):
    try:
        snip = WikiSnip.objects.get( group__name__exact = groupName,
                                     name__exact = snipName )
    except WikiSnip.DoesNotExist:
        snip = None
    return render_to_response( 'sphene/sphwiki/showSnip.html',
                               { 'snip': snip,
                                 'snipName' : snipName,
                                 },
                               context_instance = RequestContext(request) )


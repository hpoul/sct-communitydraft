from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader
from django.template.context import RequestContext
from django import newforms as forms
from django.newforms import widgets
from django.http import HttpResponse, HttpResponseRedirect


from sphene.sphwiki.models import WikiSnip


# Create your views here.


def showSnip(request, group, snipName):
    try:
        snip = WikiSnip.objects.get( group = group,
                                     name__exact = snipName )
    except WikiSnip.DoesNotExist:
        snip = None
    return render_to_response( 'sphene/sphwiki/showSnip.html',
                               { 'snip': snip,
                                 'snipName' : snipName,
                                 },
                               context_instance = RequestContext(request) )

def editSnip(request, group, snipName):
    try:
        snip = WikiSnip.objects.get( group = group,
                                     name__exact = snipName )
        SnipForm = forms.models.form_for_instance(snip)
    except WikiSnip.DoesNotExist:
        SnipForm = forms.models.form_for_model(WikiSnip)
        snip = None
    SnipForm.base_fields['body'].widget.attrs['cols'] = 80
    SnipForm.base_fields['body'].widget.attrs['rows'] = 30

    if request.method == 'POST':
        form = SnipForm(request.POST)
        if form.is_valid():
            snip = form.save(commit=False)
            snip.group = group
            snip.name = snipName
            snip.editor = request.user
            snip.save()
            return HttpResponseRedirect( '../../show/%s' % snip.name )

    else:
        form = SnipForm()

    t = loader.get_template( 'sphene/sphwiki/editSnip.html' )
    return HttpResponse( t.render( RequestContext( request, { 'form': form } ) ) )

# Create your views here.


from django import newforms as forms
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template import loader, Context

from utils.misc import cryptString, decryptString


class RegisterEmailAddress(forms.Form):
    email_address = forms.EmailField()


def register(request, group = None):

    if request.method == 'POST':
        form = RegisterEmailAddress(request.POST)
        if form.is_valid():
            regdata = form.clean_data
            email_address = regdata['email_address']
            if group:
                subject = 'Email verification required'
            else:
                subject = 'Email verification required for site %s' % group.get_name()
            validationcode = cryptString( settings.SECRET_KEY, email_address )
            t = loader.get_template('sphene/community/accounts/account_verification_email.txt')
            c = {
                'email': email_address,
                'baseurl': group.baseurl,
                'validationcode': validationcode,
                'group': group,
                }
            send_mail( subject, t.render(RequestContext(c)), None, [email_address] )
        pass
    else:
        form = RegisterEmailAddress()

    return render_to_response( 'sphene/community/register.html',
                               { 'form': form },
                               context_instance = RequestContext(request) )


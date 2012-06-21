from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from socialregistration.contrib.facebook.client import Facebook
from socialregistration.contrib.facebook.models import FacebookProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback
from socialregistration.mixins import SocialRegistration

class FacebookRedirect(OAuthRedirect):
    client = Facebook
    template_name = 'socialregistration/facebook/facebook.html'

class FacebookCallback(OAuthCallback):
    client = Facebook
    template_name = 'socialregistration/facebook/facebook.html'
    
    def get_redirect(self):
        return reverse('socialregistration:facebook:setup')

class FacebookSetup(SetupCallback):
    client = Facebook
    profile = FacebookProfile
    template_name = 'socialregistration/facebook/facebook.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'uid': client.get_user_info()['id']}

class FacebookDisconnect(SocialRegistration, View):
    def get(self, request):
        try:
            fbprofile = FacebookProfile.objects.filter(user=request.user)
        except FacebookProfile.DoesNotExist:
            pass
        else:
            fbprofile.delete()
        return HttpResponseRedirect(self.get_next(request))

from django import forms
from django.utils.translation import gettext as _

from django.contrib.auth.models import User

class UserForm(forms.Form):
    username = forms.RegexField(r'^\w+$', max_length=32)
    email = forms.EmailField(required=False)

    def __init__(self, user, profile, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user = user
        self.profile = profile

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        else:
            raise forms.ValidationError(_('This username is already in use.'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # email field of User model is not unique
            users = User.objects.filter(email=email)
            if users:
                raise forms.ValidationError(_('This email is already in use.'))
        return email

    def save(self, request=None):
        self.user.username = self.cleaned_data.get('username')
        self.user.email = self.cleaned_data.get('email')
        self.user.save()
        self.profile.user = self.user
        self.profile.save()
        return self.user

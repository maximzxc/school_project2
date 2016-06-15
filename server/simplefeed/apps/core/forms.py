from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field

from allauth.account.forms import SignupForm as AllAuthSignupForm
from allauth.account.forms import LoginForm as AllAuthLoginForm

from core.models import (
    User,
    Note,
)


class NoteUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NoteUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Edit')))

    class Meta:
        model = Note
        exclude = [
            'sender',
        ]
        fields = [
            'text',
        ]


class NoteCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NoteCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.layout.append(Submit('save', _('Create')))

    class Meta:
        model = Note
        exclude = [
            'sender',
        ]
        fields = [
            'text',
        ]


class LoginForm(AllAuthLoginForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('login_form', _('Login')))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'


class SignUpUserForm(AllAuthSignupForm):

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(SignUpUserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('signup_user_form', _('SignUp')))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.form_action = reverse('register') + '?user_type=user'
        self.helper.form_action += "&next=%s" % request.GET.get('next', '')

    def save(self, request):
        user = super(SignUpUserForm, self).save(request)
        user.save()
        return user

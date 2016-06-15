import django_filters
import django_select2

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Reset

from core.models import (
    User,
    Note,
)


class UserChoiceField(django_select2.AutoModelSelect2Field):
    queryset = User.objects.all()
    search_fields = []


class NoteChoiceField(django_select2.AutoModelSelect2Field):
    queryset = Note.objects.all()
    search_fields = ['text__icontains']


class UserChoiceFilter(django_filters.Filter):
    field_class = UserChoiceField


class NoteChoiceFilter(django_filters.Filter):
    field_class = NoteChoiceField


class NoteListViewFilter(django_filters.FilterSet):

    sender = UserChoiceFilter(
        widget=django_select2.AutoHeavySelect2Widget(
            select2_options={
                'placeholder': 'Sender',
                'minimumInputLength': 0}))

    text = django_filters.CharFilter(lookup_type="icontains")

    @property
    def form(self):
        form = super(NoteListViewFilter, self).form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.add_input(Submit('submit', 'Search'))

        return form

    class Meta:
        model = Note

        fields = [u'sender', u'text']

        exclude = []


# Have to call it clearly to help django_select2 register fields
UserChoiceField()
NoteChoiceField()

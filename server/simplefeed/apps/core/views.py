from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView
)

from pure_pagination.mixins import PaginationMixin
from braces.views import OrderableListMixin
from allauth.account.utils import complete_signup
from allauth.account.app_settings import EMAIL_VERIFICATION

from .decorators import ForbiddenUser

from .forms import LoginForm
from .forms import SignUpUserForm

from core.models import (
    User,
    Note,
)
from core.forms import (
    NoteUpdateForm,
    NoteCreateForm,
)



@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class NoteListView(PaginationMixin, ListView):

    """Note list view"""

    template_name = "note-list.html"

    model = Note
    paginate_by = 10
    orderable_columns = ["text", ]
    orderable_columns_default = "-id"

    def get_queryset(self):
        return Note.objects.filter(sender=self.request.user)


class NoteDetailView(DetailView):

    """Note detail view"""
    model = Note
    slug_field = "pk"
    template_name = "note-detail.html"

    def get_object(self, queryset=None):
        obj = super(NoteDetailView, self).get_object(queryset)
        if obj.sender.pk != self.request.user.pk:
            raise Http404("Only owner can view Note")
        return obj


class NoteUpdateView(UpdateView):

    """Note update view"""
    model = Note
    form_class = NoteUpdateForm
    slug_field = "pk"
    template_name = "note-update.html"

    def get_object(self, queryset=None):
        obj = super(NoteUpdateView, self).get_object(queryset)
        if obj.sender.pk != self.request.user.pk:
            raise Http404("Only owner can update Note")
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.save()
        return super(NoteUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Note succesfully updated"))
        return reverse("note-detail", args=[self.object.pk, ])


class NoteDeleteView(DeleteView):

    """Note delete view"""
    model = Note
    slug_field = "pk"
    template_name = "note-delete.html"

    def get_object(self, queryset=None):
        obj = super(NoteDeleteView, self).get_object(queryset)
        if obj.sender.pk != self.request.user.pk:
            raise Http404("Only owner can delete Note")
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Note succesfully deleted"))
        return reverse("note-list", args=[])


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class NoteCreateView(CreateView):

    """Note create view"""
    model = Note
    form_class = NoteCreateForm
    template_name = "note-create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.save()
        return super(NoteCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Note succesfully created"))
        return reverse("note-detail", args=[self.object.pk, ])


def login(request):
    login_form = LoginForm()

    redirect_url = reverse('note-list', args=[])
    redirect_url = request.GET.get('next') or redirect_url

    if request.method == 'POST' and 'login_form' in request.POST:
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            return login_form.login(request, redirect_url=redirect_url)

    return render(request, "login.html", {
        "login_form": login_form,
    })


def register(request):
    signup_form_user = SignUpUserForm(prefix="user", request=request)

    redirect_url = reverse('note-list', args=[])
    redirect_url = request.GET.get('next') or redirect_url

    if request.method == 'POST' and 'signup_user_form' in request.POST:
        signup_form_user = SignUpUserForm(
            request.POST,
            prefix="user",
            request=request)

        if signup_form_user.is_valid():
            user = signup_form_user.save(request)
            return complete_signup(
                request,
                user,
                EMAIL_VERIFICATION,
                redirect_url)

    return render(request, "register.html", {
        "signup_form_user": signup_form_user,
    })

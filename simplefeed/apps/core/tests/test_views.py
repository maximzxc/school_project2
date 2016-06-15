from django.core.urlresolvers import reverse
from django.utils import formats

from django_webtest import WebTest
from webtest import Upload
from model_mommy import mommy
from allauth.account.models import EmailAddress

from core.models import (
    User,
    Note,
)


class AuthTestMixin(object):

    def init_users(self):
        # Create User object
        self.user = User.objects.create(email='user@mail.com')
        self.user.set_password('test')
        self.user.save()
        # confirmation - sometimes it's required
        EmailAddress.objects.create(
            user=self.user,
            email='user@mail.com',
            primary=True,
            verified=True
        )

    def login(self, login, password):
        resp = self.app.get(reverse('account_login'))
        form = resp.forms[0]
        form['login'] = login
        form['password'] = password
        form.submit()

    def logout(self):
        resp = self.app.get('/accounts/logout/')


class NoteTest(WebTest, AuthTestMixin):

    def test_list(self):
        """Create list of Note in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        note_list = []
        note = mommy.make('core.Note', _fill_optional=True)
        note_list.append(note)

        url = reverse('note-list')

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        note_list = []
        note = mommy.make('core.Note', _fill_optional=True)
        note_list.append(note)

        url = reverse('note-list')

        self.login(self.user.email, 'test')

        url = reverse('note-list')
        resp = self.app.get(url)

        for note in note_list:
            self.assertContains(resp, note.sender)
            self.assertContains(resp, note.text)

        self.logout()

    def test_detail(self):
        """Create Note in database,
        open detail view and
        check that selected fields are visible
        """
        self.init_users()

        note = mommy.make('core.Note', _fill_optional=True)
        url = reverse('note-detail', args=(note.pk,))

        note = mommy.make(
            'core.Note',
            sender=self.anonymoususer,
            _fill_optional=True)
        url = reverse('note-detail', args=(note.pk,))

        resp = self.app.get(url)
        self.assertContains(resp, note.sender)

        self.assertContains(resp, note.text)

        note = mommy.make('core.Note', sender=self.user, _fill_optional=True)
        url = reverse('note-detail', args=(note.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        self.assertContains(resp, note.sender)

        self.assertContains(resp, note.text)

        self.logout()

    def test_udpate(self):
        """Update object using view
        Check database for updated object
        """
        self.init_users()

        note = mommy.make('core.Note', _fill_optional=True)

        url = reverse('note-update', kwargs={
            'slug': note.pk, })

        note_compare = mommy.make(
            'core.Note',
            sender=self.anonymoususer,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['text'] = note_compare.text
        form.submit()

        note_updated = Note.objects.get(pk=note.pk)

        self.assertEqual(
            note_compare.text,
            note_updated.text
        )

        self.login(self.user.email, 'test')

        note_compare = mommy.make(
            'core.Note',
            sender=self.user,
            _fill_optional=True)

        resp = self.app.get(url)

        form = resp.form
        form['text'] = note_compare.text
        form.submit()

        note_updated = Note.objects.get(pk=note.pk)

        self.assertEqual(
            note_compare.text,
            note_updated.text
        )

        self.logout()

    def test_delete(self):
        """Create Note in database,
        open delete view and
        check that object was removed
        """
        self.init_users()

        note = mommy.make('core.Note', _fill_optional=True)
        self.assertEqual(Note.objects.count(), 1)
        url = reverse('note-delete', args=(note.pk,))

        Note.objects.all().delete()

        note = mommy.make(
            'core.Note',
            sender=self.anonymoususer,
            _fill_optional=True)
        url = reverse('note-delete', args=(note.pk,))

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Note.objects.count(), 0)

        note = mommy.make('core.Note', sender=self.user, _fill_optional=True)
        url = reverse('note-delete', args=(note.pk,))
        self.login(self.user.email, 'test')

        resp = self.app.get(url)
        resp.form.submit()
        self.assertEqual(Note.objects.count(), 0)

        self.logout()

    def test_create(self):
        """Create Note object using view
        Check database for created object
        """
        self.init_users()

        note = mommy.make('core.Note', _fill_optional=True)

        url = reverse('note-create', kwargs={
        })

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        form['text'] = note.text
        form.submit()

        note_created = Note.objects.latest('id')

        self.assertEqual(
            note_created.text,
            note.text
        )

        self.logout()

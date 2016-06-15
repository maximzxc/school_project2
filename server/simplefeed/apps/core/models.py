from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django_markdown.models import MarkdownField
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_superuser, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_superuser=is_superuser,
            is_staff=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=150,
        blank=False,
        null=False,
    )
    is_staff = models.BooleanField(default=False, editable=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return unicode(self)

    def get_short_name(self):
        return unicode(self)

    def __unicode__(self):
        return unicode(self.email)

    def get_absolute_url(self):
        # TODO: add proper path
        return "/"


class Note(models.Model):
    sender = models.ForeignKey(
        'User',
        related_name='user_notes',
        blank=False,
        null=False,
    )
    text = models.TextField(blank=False)

    def __unicode__(self):
        return u"Note #%s" % self.id

    def get_absolute_url(self):
        # TODO: add proper path
        return "/"

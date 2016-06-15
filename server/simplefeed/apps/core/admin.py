from django.contrib import admin

from core.models import (
    User,
    Note,
)


# admin.site.unregister(SocialApp)
# admin.site.unregister(SocialToken)
# admin.site.unregister(SocialAccount)

admin.site.register(User)
admin.site.register(Note)

from django.contrib import admin
from .models import (
    VKUser,
    VKMessage,
)

admin.site.register(VKUser)
admin.site.register(VKMessage)



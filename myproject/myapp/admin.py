from django.contrib import admin
from .models import Questionnaires, Comment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Questionnaires)
admin.site.register(Comment)
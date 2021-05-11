from django.contrib import admin
from .models import Questionnaires, Comment, MyUser
from django.contrib.auth.admin import UserAdmin


admin.site.register(MyUser, UserAdmin)
admin.site.register(Questionnaires)
admin.site.register(Comment)
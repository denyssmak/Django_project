from rest_framework import permissions
from myapp.models import Questionnaires
from django.contrib.auth.models import User


class CommentPermisson(permissions.BasePermission):
    message = '403'

    def has_permission(self, request, view):
        if request.method in ['POST']:
            questionnaires = Questionnaires.objects.get(id=request.data['questionnaires'])
            if questionnaires.status is False:
                return False
        return True

class QuestionnairesUpdatePermisson(permissions.BasePermission):
    message = '403'

    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH']:
            user = view.get_object().user
            if request.user != user:
                return False
        return True
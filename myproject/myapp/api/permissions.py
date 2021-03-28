from rest_framework import permissions


class CommentPermisson(permissions.BasePermission):
    message = '403'

    def has_permission(self, request, view):
        if request.method in ['POST']:
            questionnaires = view.get_object().questionnaires.filter(status=False)
            if questionnaires:
                return False
        return True
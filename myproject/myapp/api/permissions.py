from rest_framework import permissions

class QuestionnairesUpdatePermisson(permissions.BasePermission):
    message = '403'

    def has_permission(self, request, view):
        if request.method in ['PATCH', 'PUT']:
            if view.get_object().session_tickets.first():
                return False
        return True
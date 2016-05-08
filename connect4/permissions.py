# Django REST Framework
from rest_framework.permissions import BasePermission

class PlayGamesPermission(BasePermission):
    def has_permission(self, request, view):
        # if I had more time I'd proper permissions for each section of the site but seeting as its just you signup
        # and play then I should allow them through.
        return request.user.is_authenticated()

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # when creating object with POST request.user will be author
        # so POST request is authorized
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True

        return obj.author.id == request.user.id

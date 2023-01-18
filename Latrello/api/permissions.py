from rest_framework import permissions


# class IsAdminOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return bool(request.user and request.user.is_staff)


class IsOwnerOrSuperuser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS and (obj.author == request.user or request.user.is_staff):
        #     return True
        return (obj.author == request.user) or bool(request.user and request.user.is_staff)

from rest_framework import permissions

# Checks if the user is the author of the entry
class IsOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True

    return obj.author == request.user

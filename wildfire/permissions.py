from rest_framework import permissions


class isOwnerOrReadOnly(permissions.BasePermission):
	#Only let the owner of an object update its information

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.owner == request.user
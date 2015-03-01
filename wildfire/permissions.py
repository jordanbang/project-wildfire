from rest_framework import permissions


class isOwnerOrReadOnly(permissions.BasePermission):
	#Only let the owner of an object update its information

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		#need to figure out some calling convention
		#needs to be checking the "userProfile" instance of the object
		return obj.owner == request.user
from rest_framework.permissions import BasePermission


class AccessTokenContributorPermission(BasePermission):
    """
    A permission which checks that the requesting user
    holds the access_token to be able to access an object.
    """

    def has_object_permission(self, request, view, obj):
        return request.auth == obj.access_token

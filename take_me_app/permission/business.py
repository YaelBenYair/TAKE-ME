from rest_framework.permissions import BasePermission
from take_me_app.models import Business


class BusinessPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST']:
            return request.user.is_authenticated and request.user.is_staff
        # if request.method in ['POST']:
        #     return False
        return True

    def has_object_permission(self, request, view, obj):
        # if request.method in ['POST']:
        #     return False
        if request.method in ['PATCH', 'PUT']:
            # print(request.user.id)
            return request.user.is_authenticated and \
                   Business.objects.filter(users=request.user.id).filter(pk=obj.id).exists()
        return True





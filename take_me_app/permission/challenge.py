from rest_framework.permissions import BasePermission
from take_me_app.models import Business, Challenge


def business_challenge_permission(request, view):
    business = Business.objects.get(pk=request.data['business'])
    return request.user.is_authenticated and \
           Business.objects.filter(users=request.user.id).filter(pk=business.id).exists()


class ChallengePermission(BasePermission):

    def has_permission(self, request, view):
        print(request.user.is_authenticated)
        if request.method in ['POST']:
            if request.data['is_business_challenge']:
                return business_challenge_permission(request, view)
            else:
                return request.user.is_authenticated
        elif request.method in ['GET', 'PATCH', 'PUT']:
            return request.user.is_authenticated

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(obj.id)
        if request.method in ['PATCH', 'PUT', 'POST']:
            if obj.is_business_challenge:
                print('business challenge')
                return request.user.is_authenticated and \
                       Business.objects.filter(users=request.user.id).filter(pk=obj.business.id).exists()

            else:
                print('user challenge')
                return request.user.is_authenticated and \
                       Challenge.objects.filter(user=request.user.id).filter(pk=obj.id)

        return request.user.is_authenticated


class ChallengeTypePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_authenticated
        else:
            return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return request.user.is_authenticated
        else:
            return request.user.is_authenticated and request.user.is_superuser






from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import status, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from take_me_app.models import Business
from take_me_app.serializers.auth import SignupSerializer, UserSerializer
from django.db.models import Q

from take_me_app.serializers.business import BusinessSerializer


class BusinessPaginationClass(PageNumberPagination):
    page_size = 3


@api_view(['POST'])
def signup(request):

    # send the data from the body to the serializer
    signup_serializer = SignupSerializer(data=request.data, many=False)

    # check the data from the user
    if signup_serializer.is_valid(raise_exception=True):
        if signup_serializer.validated_data['is_staff']:
            if not (request.user.is_authenticated and request.user.is_superuser):
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data={'is_staff': ['Only staff member can create staff user']})

        new_user = signup_serializer.create(signup_serializer.validated_data)
        user_serializer = UserSerializer(instance=new_user, many=False)
        return Response(data=user_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """
    :return: the user detail if is already authenticated
    """

    user_serializer = UserSerializer(request.user, many=False)
    return Response(data=user_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_business(request, page=None):
    """
    :return: return all the business of the user  # TODO: Pagination
    """
    business = Business.objects.filter(businessanduser__user=request.user)
    business_serializer = BusinessSerializer(business, many=True, context={'user_id': request.user.id})
    # paginator = Paginator(business_serializer, per_page=2)
    # page_object = paginator.get_page(page)
    # context = {"page_obj": page_object}
    # return render(request, context)
    return Response(business_serializer.data)


class UserPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT']:
            return request.user.is_authenticated and request.user.id == obj.id
        return True


class UserViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = User.objects.all()
    permission_classes = [UserPermissions]
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action == 'list':
            if 'user_name' in self.request.query_params:
                qs = qs.filter(Q(first_name__icontains=self.request.query_params['user_name'])
                               | Q(last_name__icontains=self.request.query_params['user_name']))
            # if 'user_last_name' in self.request.query_params:
            #     qs = qs.filter(last_name__icontains=self.request.query_params['user_last_name'])
        return qs








from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from general_func import get_tokens_for_user
from take_me_app.models import Business
from take_me_app.serializers.auth import SignupSerializer, UserSerializer, UserprofileSerializer
from django.db.models import Q

from take_me_app.serializers.business import BusinessSerializer

import uuid


class BusinessPaginationClass(PageNumberPagination):
    page_size = 3


@api_view(['POST'])
def signup(request):

    # send the data from the body to the serializer
    signup_serializer = SignupSerializer(data=request.data, many=False)

    with transaction.atomic():
        # check the data from the user
        if signup_serializer.is_valid(raise_exception=True):
            if signup_serializer.validated_data['is_staff']:
                if not (request.user.is_authenticated and request.user.is_superuser):
                    return Response(status=status.HTTP_401_UNAUTHORIZED,
                                    data={'is_staff': ['Only staff member can create staff user']})

            new_user = signup_serializer.create(signup_serializer.validated_data)
            profile = UserprofileSerializer(data={'user': new_user.id,
                                                  'profile_pic_url': None,
                                                  'is_google_login': False})
            if profile.is_valid(raise_exception=True):
                profile.save()

            user_serializer = UserSerializer(instance=new_user, many=False)
            return Response(data=user_serializer.data)
    return Response(data={}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def google_auth(request):
    CLIENT_ID = "550274521008-v682sl9vda1oetffmkvh98e1nebbvv6m.apps.googleusercontent.com"
    google_token = request.headers['Authorization']
    print('auth header: ', google_token)
    idinfo = id_token.verify_oauth2_token(google_token, requests.Request(), CLIENT_ID)
    print(idinfo)
    token = {}
    if User.objects.filter(email=idinfo['email']).exists():
        token = get_tokens_for_user(User.objects.filter(email=idinfo['email'])[0])
    else:
        password = uuid.uuid4()
        with transaction.atomic():
            signup_serializer = SignupSerializer(data={
                'email': idinfo['email'],
                'first_name': idinfo['given_name'],
                'last_name': idinfo['family_name'],
                'password': f'{password}',
                'is_staff': False
            }, many=False)

            if signup_serializer.is_valid(raise_exception=True):
                user = signup_serializer.create(signup_serializer.validated_data)
                profile = UserprofileSerializer(data={'user': user.id,
                                                      'profile_pic_url': idinfo['picture'],
                                                      'is_google_login': True})
                if profile.is_valid(raise_exception=True):
                    profile.save()
                token = get_tokens_for_user(user)

    return Response(data=token, status=status.HTTP_200_OK)


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








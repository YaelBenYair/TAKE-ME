from django.contrib.auth.models import User
from rest_framework import status, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from take_me_app.serializers.auth import SignupSerializer, UserSerializer
from django.db.models import Q


@api_view(['POST'])
def signup(request):

    # send the data from the body to the serializer
    signup_serializer = SignupSerializer(data=request.data, many=False)

    # check the data from the user
    if signup_serializer.is_valid(raise_exception=True):

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

    # permission_classes = [IsAuthenticated, IsAdminUser]
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








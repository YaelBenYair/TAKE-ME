from django.shortcuts import render, get_object_or_404
from rest_framework import status, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from take_me_app.models import Business
from take_me_app.serializers.business import BusinessSerializer, CreateAddressSerializer, \
    CreateFullBusinessSerializer, CreateBusinessChallengeSerializer


# Create your views here.


class BusinessPaginationClass(PageNumberPagination):
    page_size = 15


class BusinessPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST']:
            return request.user.is_authenticated and request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT']:
            return request.user.is_authenticated and request.user.id == obj.users.user_id
        return True


class BusinessCreateViewSet(mixins.CreateModelMixin,
                            GenericViewSet):

    queryset = Business.objects.all()

    permission_classes = [BusinessPermission]

    serializer_class = CreateFullBusinessSerializer

    pagination_class = BusinessPaginationClass

    def create(self, request, *args, **kwargs):
        data_copy = request.data.copy()
        data_copy['user_id'] = request.user.id
        print(data_copy)
        serializer = self.get_serializer(data=data_copy, partial=True)
        serializer.is_valid(raise_exception=True)
        business = serializer.save()
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        response_serializer = BusinessSerializer(business, context={'request': request,
                                                                    'user_id': data_copy['user_id']})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class BusinessViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):

    queryset = Business.objects.all()

    permission_classes = [BusinessPermission]

    serializer_class = BusinessSerializer

    pagination_class = BusinessPaginationClass

    def get_queryset(self):
        qs = self.queryset
        if self.action == 'list':
            if 'name' in self.request.query_params:
                qs = qs.filter(name__icontains=self.request.query_params['name'])
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@api_view(['POST', 'GET'])
# @permission_classes([BusinessPermission])
def business_challenge(request, business_id):
    get_object_or_404(Business, id=business_id)

    if request.method == 'POST':
        business_serializer = CreateBusinessChallengeSerializer(data=request.data, many=False,
                                                            context={'business_id': business_id, 'request': request})
        if business_serializer.is_valid():
            business = business_serializer.create(business_serializer.validated_data)

        # op_houer = CreateOpeningHours()
        # if address.is_valid():
        #     address_value = address.create(address.validated_data)
        # return Response(data=address.data)


@api_view(['POST'])
def create_business_challenge(request):
    pass

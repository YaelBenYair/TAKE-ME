from django.shortcuts import render
from rest_framework import status, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from take_me_app.models import Business
from take_me_app.serializers.business import BusinessSerializer, CreateAddressSerializer, \
    CreateFullBusinessSerializer


# Create your views here.

# @api_view(['POST'])
# def create_business(request):
#     business_serializer = CreateBusinessSerializer(data=request.data, many=False)
#     if business_serializer.is_valid():
#         business = business_serializer.create(business_serializer.validated_data)
#         address = CreateAddressSerializer(many=False, data=request.data, context={'business': business,
#                                                                                  'request': request})
#         # op_houer = CreateOpeningHours()
#         if address.is_valid():
#             address_value = address.create(address.validated_data)
#         return Response(data=address.data)


# @api_view(['POST'])
# # @permission_classes([BusinessPermission])
# def create_business(request):
#     data_copy = request.data.copy()
#     data_copy['user_id'] = request.user.id
#     business_serializer = CreateFullBusinessSerializer(data=data_copy, partial=True)
#     if business_serializer.is_valid(raise_exception=True):
#         business_serializer.save()
#         return Response()
#     return Response(status=status.HTTP_400_BAD_REQUEST)


class BusinessPaginationClass(PageNumberPagination):
    page_size = 3


class BusinessPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['POST']:
            return request.user.is_authenticated and request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT']:
            return request.user.is_authenticated and request.user.id == obj.users.user_id


class BusinessCreateViewSet(mixins.CreateModelMixin,
                            GenericViewSet):

    queryset = Business.objects.all()

    permission_classes = [BusinessPermission]

    serializer_class = CreateFullBusinessSerializer

    pagination_class = BusinessPaginationClass

    def get_queryset(self):
        qs = self.queryset
        if self.action == 'list':
            if 'name' in self.request.query_params:
                qs = qs.filter(name__icontains=self.request.query_params['name'])

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

    # pagination_class = BusinessPaginationClass

    # def get_queryset(self):
    #     qs = self.queryset
    #     if self.action == 'list':
    #         if 'name' in self.request.query_params:
    #             qs = qs.filter(name__icontains=self.request.query_params['name'])

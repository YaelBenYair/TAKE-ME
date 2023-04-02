from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator

from take_me_app.models import Business, Address, OpeningHours, BusinessAndUser, BusinessAccessibility, BusinessAndType


class BusinessSerializer(serializers.ModelSerializer):

    user_name = serializers.SerializerMethodField('get_user_name')
    address = serializers.SerializerMethodField('get_address')

    class Meta:
        model = Business
        fields = ['id', 'name', 'description', 'phone_num', 'menu_url', 'load_hour', 'user_name', 'address']

    def get_user_name(self, obj):
        # user = User.objects.get(pk=self.context['user_id'])
        b = Business.objects.filter(id=obj.id).values_list('businessanduser__user__first_name',
                                                           'businessanduser__user__last_name')
        # user = BusinessAndUser.objects.get(business_id=obj.id)
        # return obj.users.first_name + obj.users.last_name
        return b[0][0] + " " + b[0][1]

    def get_address(self, obj):
        address = Address.objects.get(business_id=obj.id)
        return f"{address.city}, {address.street} {address.number}"


class CreateAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class CreateOpeningHoursSerializer(serializers.ModelSerializer):

    class Meta:
        model = OpeningHours
        fields = '__all__'


class BusinessAndUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessAndUser
        fields = '__all__'


class BusinessAccessibilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessAccessibility
        fields = '__all__'


class BusinessAndTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessAndType
        fields = '__all__'


# class UserIdSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField()
#     class Meta:
#         model = User
#         fields = ['id']


class CreateFullBusinessSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(write_only=True)
    address = CreateAddressSerializer(many=False)
    opening_hours = CreateOpeningHoursSerializer(many=True)
    business_and_type = BusinessAndTypeSerializer(many=True)
    # business_and_user = BusinessAndUserSerializer(many=False)
    business_accessibility = BusinessAccessibilitySerializer()

    class Meta:
        model = Business
        fields = ['name', 'description', 'phone_num', 'menu_url', 'load_hour', 'user_id', 'address',
                  'opening_hours', 'business_and_type', 'business_accessibility']

    def create(self, validated_data):
        print("in create", validated_data)
        address_data = validated_data.pop('address')
        opening_hours_data = validated_data.pop('opening_hours')
        user_id_data = validated_data.pop('user_id')
        business_and_types_data = validated_data.pop('business_and_type')
        # business_and_user_data = validated_data.pop('business_and_user')
        business_accessibility_data = validated_data.pop('business_accessibility')

        print("after pop", validated_data)

        business = Business.objects.create(**validated_data)

        Address.objects.create(business=business, **address_data)
        BusinessAndUser.objects.create(business=business, user_id=user_id_data)
        BusinessAccessibility.objects.create(business=business, **business_accessibility_data)

        # date_format = '%H:%M'
        for opening_hour_data in opening_hours_data:
            OpeningHours.objects.create(business=business, **opening_hour_data)

        for business_type_data in business_and_types_data:
            BusinessAndType.objects.create(business=business, **business_type_data)

        return business


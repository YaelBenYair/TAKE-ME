from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator

from take_me_app.models import UserProfile


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_staff')

    email = serializers.EmailField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        allow_null=False,
        allow_blank=False,
        validators=[validate_password]
    )

    first_name = serializers.CharField(
        write_only=True,
        required=True,
        allow_null=False,
        allow_blank=False
    )

    last_name = serializers.CharField(
        write_only=True,
        required=True,
        allow_null=False,
        allow_blank=False
    )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=validated_data['is_staff']
        )

        # hash password
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'id', 'userprofile',
                  'user_address', 'is_staff', 'is_superuser')
        depth = 1
        extra_kwargs = {
            'userprofile': {
                'read_only': True
            }
        }


class UserprofileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('user', 'profile_pic_url', 'is_google_login')


# class EmailCheckSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ['email']





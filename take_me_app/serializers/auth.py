from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator



class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    email = serializers.EmailField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        allow_null=False,
        allow_blank=False
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
        )

        # hash password
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'id')




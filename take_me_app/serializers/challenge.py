from datetime import datetime

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator

from take_me_app.models import Challenge, BusinessChallengeDetails, WhoToChallenge, ChallengeType


class ChallengeBusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessChallengeDetails
        fields = ['end_date']


class CreateBusinessChallengeSerializer(serializers.ModelSerializer):

    business_challenge_detail = ChallengeBusinessSerializer(many=False)

    class Meta:
        model = Challenge
        fields = ['business', 'name', 'challenge_type', 'date', 'challenge_time', 'text_on_challenge',
                  'is_business_challenge', 'business_challenge_detail']

    def create(self, validated_data):
        with transaction.atomic():
            b_challenge_d = validated_data.pop('business_challenge_detail')

            # b_challenge = Challenge.objects.create(business_id=self.context['business_id'], **validated_data)
            b_challenge = Challenge.objects.create(**validated_data)

            BusinessChallengeDetails.objects.create(challenge=b_challenge, **b_challenge_d)

            return b_challenge


class GetBusinessChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Challenge
        fields = ['id', 'name', 'business_id', 'challenge_type', 'date', 'challenge_time', 'text_on_challenge',
                  'is_business_challenge', 'business_details']
        depth = 1


class CreateUserChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Challenge
        fields = ['user', 'business', 'name', 'challenge_type', 'date', 'challenge_time', 'text_on_challenge',
                  'is_business_challenge']


class WhoToChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WhoToChallenge
        fields = ['user', 'challenge', 'answer', 'who_challenge', 'is_read']


class GetUserChallengeSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField('get_user_name')

    class Meta:
        model = Challenge
        fields = ['id', 'user_id', 'user_name', 'name', 'challenge_type', 'date', 'challenge_time', 'text_on_challenge',
                  'is_business_challenge', 'who_challenged']
        depth = 1

    @staticmethod
    def get_user_name(obj):
        b = Challenge.objects.filter(id=obj.id).values_list('user__first_name',
                                                           'user__last_name')
        return b[0][0] + " " + b[0][1]


class ChallengeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChallengeType
        fields = '__all__'








from datetime import datetime

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator

from take_me_app.models import Challenge, BusinessChallengeDetails, WhoToChallenge


class ChallengeBusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessChallengeDetails
        fields = ('start_date', 'end_date')


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
        fields = ['id', 'name', 'challenge_type', 'date', 'challenge_time', 'text_on_challenge',
                  'is_business_challenge', 'business_details']
        depth = 1


class CreateUserChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Challenge
        fields = ['user', 'business', 'name', 'challenge_type', 'date', 'challenge_time', 'text_on_challenge',
                  'is_business_challenge']

# ser = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='accepts_challenge')
#     challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, null=False, blank=False)
#     answer = models.BooleanField(db_column='answer', null=False, blank=False)
#     who_challenge = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,
#                                       related_name='Sender_challenge')
#     is_read

class WhoToChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WhoToChallenge
        fields = ['user', 'challenge', 'answer', 'who_challenge', 'is_read']


class GetUserChallengeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Challenge
        fields = ['id', 'name', 'challenge_type', 'date', 'challenge_time', 'text_on_challenge',
                  'is_business_challenge']
        depth = 1








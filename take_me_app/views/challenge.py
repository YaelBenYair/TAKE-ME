from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from take_me_app.models import Challenge
from take_me_app.serializers.challenge import CreateBusinessChallengeSerializer, GetBusinessChallengeSerializer, \
    CreateUserChallengeSerializer, GetUserChallengeSerializer, WhoToChallengeSerializer


class CreateChallengeViewSet(ModelViewSet):

    queryset = Challenge.objects.all()

    # serializer_class = GetBusinessChallengeSerializer

    def get_serializer_class(self):
        if self.action in ['list']:
            if self.request.query_params['is_business']:
                return GetBusinessChallengeSerializer
            else:
                return GetUserChallengeSerializer
    def get_queryset(self):
        qs = self.queryset
        if self.action == 'list':
            if 'is_business' in self.request.query_params:
                qs = qs.filter(is_business_challenge=self.request.query_params['is_business'])
            elif 'business_id' in self.request.query_params:
                qs = qs.filter(business=self.request.query_params['business_id'])
            elif 'user_id' in self.request.query_params:
                qs = qs.filter(user=self.request.query_params['user_id'])
            elif 'range_date_now' in self.request.query_params:
                qs = qs.filter(business_details__end_date__gte=self.request.query_params['range_date_now'])
    def create(self, request, *args, **kwargs):
        if request.data['is_business_challenge'] is True:

            serializer = CreateBusinessChallengeSerializer(data=request.data, many=False)

            if serializer.is_valid(raise_exception=True):
                business_ch = serializer.create(serializer.validated_data)
                view_business_ch = GetBusinessChallengeSerializer(business_ch, many=False)
                return Response(data=view_business_ch.data)

        else:
            who_to_chall = request.data.pop('who_to_challenge')
            print("In create user challenge")

            data_copy = request.data.copy()
            data_copy['user'] = request.user.id

            print(who_to_chall)
            with transaction.atomic():

                # create user challenge
                serializer = CreateUserChallengeSerializer(data=data_copy, many=False)
                if serializer.is_valid(raise_exception=True):
                    user_challenge = serializer.create(serializer.validated_data)

                    for user_chall in who_to_chall:
                        user_chall.update({"who_challenge": request.user.id})
                        user_chall.update({"challenge": user_challenge.id})

                    # add the friends that the user want to challenge
                    users_challenged_serializer = WhoToChallengeSerializer(data=who_to_chall, many=True)
                    if users_challenged_serializer.is_valid(raise_exception=True):
                        users_challenged_serializer.save()

                    view_user_ch = GetUserChallengeSerializer(user_challenge, many=False)
                    return Response(data=view_user_ch.data)

                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={
                        "status": 400,
                        "data": "the request is not valid"
                    })


@api_view(['POST'])
def add_users_to_business_challenge(request):
    pass










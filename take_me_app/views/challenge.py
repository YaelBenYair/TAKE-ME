from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status, mixins

from take_me_app.models import Challenge, WhoToChallenge, ChallengeType
from take_me_app.permission.challenge import ChallengePermission, ChallengeTypePermission
from take_me_app.serializers.challenge import CreateBusinessChallengeSerializer, GetBusinessChallengeSerializer, \
    CreateUserChallengeSerializer, GetUserChallengeSerializer, WhoToChallengeSerializer, ChallengeTypeSerializer


class CreateChallengeViewSet(
    # ModelViewSet
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):

    queryset = Challenge.objects.all()
    permission_classes = [ChallengePermission]

    # serializer_class = GetBusinessChallengeSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action in ['list']:
            if self.request.query_params['is_business']:
                return GetBusinessChallengeSerializer(*args, **kwargs)
            else:
                return GetUserChallengeSerializer(*args, **kwargs)
        elif self.action == 'retrieve':
            if args[0].is_business_challenge is True:
                return GetBusinessChallengeSerializer(*args, **kwargs)
            else:
                return GetUserChallengeSerializer(*args, **kwargs)
        elif self.action in ['partial_update', 'update']:
            if args[0].is_business_challenge is True:
                return CreateBusinessChallengeSerializer(*args, **kwargs)
            else:
                return CreateUserChallengeSerializer(*args, **kwargs)

    def get_queryset(self):
        qs = self.queryset
        if self.action == 'list':
            if 'is_business' in self.request.query_params:
                qs = qs.filter(is_business_challenge=self.request.query_params['is_business'])
            if 'business_id' in self.request.query_params:
                qs = qs.filter(business=self.request.query_params['business_id'])
            if 'user_id' in self.request.query_params:
                qs = qs.filter(user=self.request.query_params['user_id'])
            if 'range_date_now' in self.request.query_params:
                qs = qs.filter(business_details__end_date__gte=self.request.query_params['range_date_now'])

        return qs

    # def update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if 'is_business' not in request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    'status': 400,
                    'data': 'is_business - filed required'
                })
        else:
            return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if request.data['is_business_challenge']:

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


# @api_view(['POST'])
# def add_users_to_exists_challenge(request):
#     data_copy = request.data.copy()
#     for user_challenge in data_copy:
#         user_challenge.update({"who_challenge": request.user.id})
#     user_challenge_serializer = WhoToChallengeSerializer(data=data_copy, many=True)
#     if user_challenge_serializer.is_valid(raise_exception=True):
#         user_challenge_serializer.save()
#         return Response(data=user_challenge_serializer.data)
#
#     return Response(status=status.HTTP_400_BAD_REQUEST, data={
#         "status": 400,
#         "data": "invalid data",
#     })
#     pass


class WhoToChallengeViewSet( mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              # mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              GenericViewSet):

    queryset = WhoToChallenge.objects.all()

    serializer_class = WhoToChallengeSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action == 'list':
            if 'user' in self.request.query_params:
                if self.request.query_params['user']:
                    qs = qs.filter(user=self.request.user)
            if 'challenge' in self.request.query_params:
                qs = qs.filter(challenge=self.request.query_params['challenge'])
            if 'who_challenge' in self.request.query_params:
                qs = qs.filter(who_challenge=self.request.query_params['who_challenge'])
            if 'answer' in self.request.query_params:
                qs = qs.filter(answer=self.request.query_params['answer'])

        return qs

    def create(self, request, *args, **kwargs):
        data_copy = request.data.copy()
        for user_challenge in data_copy:
            user_challenge.update({"who_challenge": request.user.id})
        user_challenge_serializer = WhoToChallengeSerializer(data=data_copy, many=True)
        if user_challenge_serializer.is_valid(raise_exception=True):
            user_challenge_serializer.save()
            return Response(data=user_challenge_serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            "status": 400,
            "data": "invalid data",
        })


class ChallengeTypeViewSet(ModelViewSet):

    queryset = ChallengeType.objects.all()
    permission_classes = [ChallengeTypePermission]
    serializer_class = ChallengeTypeSerializer

    # TODO: create function with boto3 (aws s3)




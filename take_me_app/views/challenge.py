from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from take_me_app.models import Challenge


class CreateChallengeViewSet(ModelViewSet):
    queryset = Challenge.objects.all()




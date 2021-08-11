from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import *
User = get_user_model()


class RegisterView(APIView):

    def post(self, req):
        data = req.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Success!', status=status.HTTP_201_CREATED)


class ActivationView(APIView):

    def get(self, req, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Succsessfully activated!', status=status.HTTP_200_OK)


# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#
#     def get_serializer_class(self):
#         pass

# TODO: login
# TODO: logout
# TODO: TOKEN: base, sessions, token - json web tokens


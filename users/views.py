from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import *
User = get_user_model()


class RegisterView(APIView):

    def post(self, req):
        data = req.data
        serializer = RegistrationSerializer(data=data)
        data_ = {}
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data_['email'] = user.email
            data_['name'] = user.name
            data_['lastname'] = user.lastname
            token = Token.objects.get(user=user).key
            data_['token'] = token
            return Response(data_, status=status.HTTP_201_CREATED)


class ActivationView(APIView):

    def get(self, req, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Sucsessfully activated!', status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = UserSerializer


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, req):
        user = req.user
        Token.objects.filter(user=user).delete()
        return Response('Logged Out!', status=status.HTTP_200_OK)




class ForgotPasswordView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        user = get_object_or_404(User, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code(email=user.email,
                             activation_code=user.activation_code,
                             status='reset_password')
        return Response('Вам отправили письмо на почту', status=200)


class CompleteResetPassword(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно восстановили пароль', status=200)


from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer, ActivationSerializer, ChangePasswordSerializer, ForgotPasswordSerializer,RebuildForgottenPasswordSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .permissions import IsActivePermission
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from collections import OrderedDict

# Create your views here.


class RegistrationView(APIView):

    @swagger_auto_schema(request_body=RegistrationSerializer())
    def post(self, request):
        serialzer = RegistrationSerializer(data = request.data)
        serialzer.is_valid(raise_exception=True)
        serialzer.save()
        return Response('Аккаунт успешно создан', status=201)


class ActivationView(APIView):
    @swagger_auto_schema(request_body=ActivationSerializer())
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response('Аккаунт успешно активирован', status=200)
    

class LoginView(ObtainAuthToken):
    
    serializer_class = LoginSerializer


class LogoutView(APIView):

    permission_classes = [IsActivePermission]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы разлогинились.')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=ChangePasswordSerializer())
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request':request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Пароль успешно обновлен')


class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer())
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('Вам выслан сообщение для восстановления пароля')


class RebuildForgottenPasswordView(APIView):
    @swagger_auto_schema(request_body=RebuildForgottenPasswordSerializer())
    def post(self,request):
        serialiser = RebuildForgottenPasswordSerializer(data=request.data)

        if serialiser.is_valid(raise_exception=True):
            serialiser.set_new_password()
            return Response('Пароли успешно установлен')

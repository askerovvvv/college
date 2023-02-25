from django.shortcuts import render
# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse

# from rest_framework.authtoken.views import ObtainAuthToken
#
#
# class LoginView(ObtainAuthToken):
#     serializer_class = LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from account.serializers import ForgotPasswordSerializer, ForgotPasswordCompleteSerializer

User = get_user_model()


class ActivationView(APIView):
    """
    If program can find user with that activation_code the user will be 'is_active' and after can
    login_ to the site
    """
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return HttpResponse("YOU have successfully activated your account")
        except User.DoesNotExist:
            return HttpResponse("Activation code is not valid")


class ForgotPasswordApiView(APIView):
    """
    It will send activation code to user's email he must save it
    """
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response('An activation code has been sent to you to change your password.!')


class ForgotPasswordCompleteApiView(APIView):
    """
    user writes activation code that has sent before and after user can change password
    """
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create_new_password()
            return Response('Password updated successfully')




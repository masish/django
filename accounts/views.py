from django.contrib.auth import login, authenticate
from rest_framework import authentication, permissions, generics

from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.db import transaction
from django.http import HttpResponse, Http404
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView

from .serializer import UserSerializer, UserSerializerCreate, UserSerializerUpdate
from .models import User, UserManager

from django.shortcuts import render, redirect

from .forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('top')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


# ユーザ作成のView(POST)
class AuthRegister(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializerCreate

    @transaction.atomic
    def post(self, request, format=None):
        serializer = UserSerializerCreate(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ユーザ情報更新のView(PUT)
class AuthInfoUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializerUpdate
    queryset = User.objects.all()

    def get_object(self):
        try:
            instance = self.queryset.get(id=self.request.user.id)
            return instance
        except User.DoesNotExist:
            raise Http404


# ユーザ情報取得のView(GET)
class AuthInfoGetView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, format=None):
        return Response(data={
            'username': request.user.username,
            'email': request.user.email,
            },
            status=status.HTTP_200_OK)

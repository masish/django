from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from .models import User, UserManager


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'self_introduction', 'display_name', 'profile_icon')


class UserSerializerCreate(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id',
                    'username',
                    'email',
                    'self_introduction',
                    'display_name',
                    'profile_icon',
                    'password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializerUpdate(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'self_introduction', 'display_name', 'profile_icon', 'password')

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        else:
            instance = super().update(instance, validated_data)
        instance.save()
        return instance
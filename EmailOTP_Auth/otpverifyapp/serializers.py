from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_verified']

    def create(self, validated_data):
        user = CustomUser.objects.create(email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
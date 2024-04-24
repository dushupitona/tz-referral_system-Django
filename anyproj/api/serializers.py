from rest_framework import serializers
from referral.models import User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number']



class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']
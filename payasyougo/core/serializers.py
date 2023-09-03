from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import *


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists.')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email address already in use.')

        try:
            validate_password(password, user=User)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return data


class UserAuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class UserRequestCountSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='user__id')
    username = serializers.CharField(source='user__username')
    request_count = serializers.IntegerField()


class TotalPriceSerializer(serializers.Serializer):
    user = serializers.CharField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=4)


class CurrentMonthCostSerializer(serializers.Serializer):
    user = serializers.CharField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=4)

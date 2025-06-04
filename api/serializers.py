from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account
# from .utils import SendMail
from django.contrib.sites.shortcuts import get_current_site



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            'user', 'first_name', 'last_name', 'phone',
            'email', 'date_created', 'avatar', 'avatar_url',
        ]
        
    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return request.build_absolute_uri(obj.avatar.url)
        return None


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'password1', 'password2', 'phone'
        ]

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username already exists')
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email already exists')
        if Account.objects.filter(phone=data.get('phone')).exists():
            raise serializers.ValidationError('Phone number already exists')
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        user.save()

        account = Account.objects.create(
            user=user,
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone=validated_data.get('phone'),
            email=email,
        )

        fullname = f"{account.first_name} {account.last_name}"
        # SendMail(email, fullname)

        return account
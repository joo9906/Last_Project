# accounts/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

# 회원가입 전용 (비밀번호 write_only)
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'language', 'manager']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            language=validated_data.get('language', 'en'),
            manager=validated_data.get('manager', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# 조회, 수정용
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

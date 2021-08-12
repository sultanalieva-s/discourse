# TODO: Registration serializer, Login serializer, User List, User Detail, User Update
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.utils import send_activation_code

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirm = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'name', 'lastname', 'about', 'organization',)

    def validate(self, validated_data):
        password_confirm = validated_data.pop('password_confirm')
        password = validated_data.get('password')

        if password != password_confirm:
            raise serializers.ValidationError('Password confirmation does not match')

        return validated_data

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')

        user = User.objects.create_user(email=email, password=password, **validated_data)

        send_activation_code(email=user.email, activation_code=user.activation_code)

        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(label='Password', style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError('Wrong credentials', code='authorization')
        else:
            raise serializers.ValidationError('Must include email and password', code='authorization')

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'lastname')


















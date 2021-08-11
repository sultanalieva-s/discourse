# TODO: Registration serializer, Login serializer, User List, User Detail, User Update
from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.utils import send_activation_code

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, read_only=True)
    password_confirm = serializers.CharField(min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'name', 'lastname', 'about', 'organization',)

    def validate(self, validated_data):
        password_confirm = validated_data.get('password_confirm')
        password = validated_data.get('password')

        if password != password_confirm:
            raise serializers.ValidationError('Password confirmation does not match')

        return validated_data

    def create(self, validated_data):
        password = validated_data.get('password')
        email = validated_data.pop('email')

        user = User.objects.create_user(email=email, password=password, **validated_data)

        send_activation_code(email=user.email, activation_code=user.activation_code)

        return user










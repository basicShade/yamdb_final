import re
from secrets import token_urlsafe

from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SignUpNewSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value == 'me':
            raise exceptions.ValidationError(
                'Имя пользователя не может быть <me>.',
            )
        if re.search(r'^[\w.@+-]+$', value) is None:
            raise exceptions.ValidationError(
                'Недопустимые символы в username.',
            )
        return value

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')

        user = User.objects.create(
            username=username,
            email=email
        )
        user.is_active = False
        user.role = 'user'
        user.confirmation_code = token_urlsafe(8)

        user.save()
        attrs['user'] = user

        return attrs


class SignUpExistingSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        user = User.objects.get(username=username)

        if user.email == email:
            user.confirmation_code = token_urlsafe(8)
        else:
            raise exceptions.ParseError('Почта не совпадает')

        user.save()
        attrs['user'] = user

        return attrs


class ConfCodeAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound('Пользователь не найден')

        if confirmation_code != user.confirmation_code:
            raise serializers.ValidationError('Реквизиты не совпадают')

        attrs['user'] = user
        attrs['confirmation_code'] = confirmation_code

        return attrs


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta():
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    def validate_username(self, value):
        if not bool(re.match(r'^[\w.@+-]+$', value)):
            raise serializers.ValidationError(
                "Используются некорректные символы"
            )
        return value

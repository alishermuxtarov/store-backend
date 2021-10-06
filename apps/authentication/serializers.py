from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext as _

from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authentication.utils.serializers import ValidatorSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=True)

    @staticmethod
    def get_permissions(user):
        return user.get_all_permissions()

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'permissions', 'password')
        extra_kwargs = {
            'email': {
                'validators': [UniqueValidator(queryset=User.objects.all())]
            }
        }


class LoginValidator(ValidatorSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)

    def validate(self, data):
        user = User.objects.filter(username=data.get('username')).first()

        if user:
            if not user.is_active:
                raise ValidationError({'username': _("Пользователь не активен")})

            if not user.check_password(data.get('password')):
                raise AuthenticationFailed({'password': _("Неверный пароль")})

            return data, user
        else:
            raise AuthenticationFailed({'username': _("Пользователь не существует")})


class LoginDataSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()

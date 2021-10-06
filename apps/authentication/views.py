from django.utils import timezone

from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import LoginValidator, LoginDataSerializer, UserSerializer
from .models import Token, User


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginValidator

    def post(self, request):
        _, user = self.serializer_class.check(request.data)
        token, _ = Token.objects.get_or_create(user=user)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return Response(LoginDataSerializer(instance={'token': token.key, 'user': user}).data)


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

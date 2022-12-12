from django.core.mail import EmailMessage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.permisions import AdminOnly

from .serializers import (SignUpNewSerializer,
                          SignUpExistingSerializer,
                          ConfCodeAuthTokenSerializer,
                          UserSerializer)
from .models import User


class APISignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        if username and not User.objects.filter(username=username).exists():
            serializer = SignUpNewSerializer(data=request.data)
        else:
            serializer = SignUpExistingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        to_email = user.email
        mail_subject = 'Confirmation_code has been sent to your email id'
        message = (
            'Подтвердите email:{email},'
            'для этого отправте confirmation_code:{confirmation_code}'
            .format(email=to_email,
                    confirmation_code=user.confirmation_code)
        )
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfCodeAuthToken(APIView):
    permission_classes = [AllowAny]
    serializer_class = ConfCodeAuthTokenSerializer

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.is_active = True
        user.save()

        token = str(self.get_token(user).access_token)

        return Response(
            data={'token': token},
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    permission_classes = [AdminOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', ],
        permission_classes=[AllowAny],
        url_path='me',
        url_name='me'
    )
    def user_profile(self, request):
        if request.method == 'GET':
            if not isinstance(request.user, User):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            if not isinstance(request.user, User):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                if request.user.role == 'user':
                    serializer.validated_data['role'] = 'user'
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

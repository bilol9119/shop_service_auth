from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime, timedelta
from .models import MicroServiceToken, OneTimeToken


class TokenViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Check token",
        operation_summary="Check microservices token ",
        responses={200: 'ok'},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'secret_token': openapi.Schema(type=openapi.TYPE_STRING, maxLength=100),
            },
            required=['secret_token']
        ),
        tags=['token_check']

    )
    def check_token(self, request, *args, **kwargs):
        secret_token = request.data.get('secret_token')

        obj = OneTimeToken.objects.filter(secret_token=secret_token).first()
        if not obj:
            return Response({"error": "token not found"}, status=status.HTTP_404_NOT_FOUND)

        if not self.check_token_expire(obj.created_at):
            return Response({"error": "token expired"}, status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "ok"}, status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="one-time Token create ",
        operation_summary="Create token",
        responses={201: "secret_token"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'secret_service_key': openapi.Schema(type=openapi.TYPE_STRING, maxLength=100),
            },
            required=['secret_service_key']
        ),
        tags=['token_create']

    )
    def create_token(self, request, *args, **kwargs):
        secret_service_key = request.data.get('secret_service_key')

        obj = MicroServiceToken.objects.filter(secret_key=secret_service_key).first()
        if not obj:
            return Response({"error": "service not found"}, status.HTTP_404_NOT_FOUND)

        one_time_token = OneTimeToken.objects.create(micro_service=obj)
        one_time_token.save()
        return Response({"secret_token": one_time_token.secret_token}, status.HTTP_201_CREATED)

    def check_token_expire(self, created_at):
        current_time = datetime.now()
        if current_time - created_at > timedelta(minutes=1):
            return False
        return True

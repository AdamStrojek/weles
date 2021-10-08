from typing import List, Dict, Text, Any

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.fields import DateField
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import SecretSerializer, SecretPasswordSerializer
from ..models import Secret, SecretAccessLog


class SecretViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        qs = Secret.objects.all()
        match self.action:
            case 'list' | 'retrieve':
                return qs.filter(user=self.request.user)
            case 'create':
                return qs

    serializer_class = SecretSerializer
    password_serializer_class = SecretPasswordSerializer

    @action(detail=True, methods=['post'])
    def access(self, request, pk=None):
        instance = self.get_object()

        context = {
            'instance': instance
        }
        passwd_serializer = self.password_serializer_class(data=request.data, context=context)
        passwd_serializer.is_valid(raise_exception=True)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SecretAccessLogViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SecretAccessLog.objects.filter(secret__user=self.request.user).statistics()

    def process_data(self, input_data: List[Dict[Text, Any]]):
        output = {}  # Since python 3.7 order of items will be guaranteed
        date_converter = DateField()

        for item in input_data:
            date = date_converter.to_representation(item.pop('date'))
            output[date] = item

        return output

    def list(self, request):
        data = self.get_queryset()

        output_data = self.process_data(data)

        return Response(output_data)

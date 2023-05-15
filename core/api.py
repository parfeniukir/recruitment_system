from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.models import Application, Job
from core.serializers import ApplicationSerializer, JobSerializer

User = get_user_model()


class JobsAPISet(ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.all()

    def list(self, request):
        raise APIException("This feature is not supported yet")


class ApplicationsListAPI(ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

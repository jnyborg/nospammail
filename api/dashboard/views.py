from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from dashboard.models import GeneratedEmail
from dashboard.permissions import IsOwnerOrReadOnly
from dashboard.serializers import GeneratedEmailSerializer, UserSerializer


class GeneratedEmailViewSet(viewsets.ModelViewSet):
    queryset = GeneratedEmail.objects.all()
    serializer_class = GeneratedEmailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    # Set the owner to current logged in user on create.
    def perform_create(self, serializer):
        article = serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = User.objects.all()
    serializer_class = UserSerializer



from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .serializers import VoterSerializer
from .models import Voter


class VoterViewSet(ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    permission_classes = (AllowAny,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

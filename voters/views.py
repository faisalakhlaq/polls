from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .serializers import VoterSerializer
from .models import Voter


class VoterViewSet(ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    permission_classes = (AllowAny,)

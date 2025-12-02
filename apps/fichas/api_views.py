from rest_framework import viewsets, permissions
from .models import NPC, Monstro
from .serializers import NPCSerializer, MonstroSerializer
class NPCViewSet(viewsets.ModelViewSet):
    queryset = NPC.objects.all()
    serializer_class = NPCSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class MonstroViewSet(viewsets.ModelViewSet):
    queryset = Monstro.objects.all()
    serializer_class = MonstroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

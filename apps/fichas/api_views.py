from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'tipo', 'alignment', 'source']
    ordering_fields = ['nome', 'cr', 'ac', 'hp_media']
    ordering = ['nome']
    
    def get_queryset(self):
        queryset = Monstro.objects.all()
        
        # Filtrar por tipo
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            queryset = queryset.filter(tipo__iexact=tipo)
        
        # Filtrar por tamanho
        tamanho = self.request.query_params.get('tamanho', None)
        if tamanho:
            queryset = queryset.filter(tamanho=tamanho)
        
        # Filtrar por CR
        cr = self.request.query_params.get('cr', None)
        if cr:
            queryset = queryset.filter(cr=cr)
        
        # Filtrar por CR mínimo
        cr_min = self.request.query_params.get('cr_min', None)
        if cr_min:
            # Conversão simplificada de CR para número para comparação
            try:
                cr_min_float = float(cr_min)
                # IDs dos CRs em ordem crescente
                cr_order = {
                    '0': 0, '1/8': 0.125, '1/4': 0.25, '1/2': 0.5,
                    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                    '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12,
                    '13': 13, '14': 14, '15': 15, '16': 16, '17': 17,
                    '18': 18, '19': 19, '20': 20, '21': 21, '22': 22,
                    '23': 23, '24': 24, '25': 25, '26': 26, '27': 27,
                    '28': 28, '29': 29, '30': 30
                }
                valid_crs = [cr for cr, val in cr_order.items() if val >= cr_min_float]
                queryset = queryset.filter(cr__in=valid_crs)
            except:
                pass
        
        # Filtrar por CR máximo
        cr_max = self.request.query_params.get('cr_max', None)
        if cr_max:
            try:
                cr_max_float = float(cr_max)
                cr_order = {
                    '0': 0, '1/8': 0.125, '1/4': 0.25, '1/2': 0.5,
                    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                    '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12,
                    '13': 13, '14': 14, '15': 15, '16': 16, '17': 17,
                    '18': 18, '19': 19, '20': 20, '21': 21, '22': 22,
                    '23': 23, '24': 24, '25': 25, '26': 26, '27': 27,
                    '28': 28, '29': 29, '30': 30
                }
                valid_crs = [cr for cr, val in cr_order.items() if val <= cr_max_float]
                queryset = queryset.filter(cr__in=valid_crs)
            except:
                pass
        
        # Filtrar por AC
        ac = self.request.query_params.get('ac', None)
        if ac:
            queryset = queryset.filter(ac=ac)
        
        # Filtrar por source/livro
        source = self.request.query_params.get('source', None)
        if source:
            queryset = queryset.filter(source__iexact=source)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def filtros_disponiveis(self, request):
        """Retorna opcões de filtro disponíveis"""
        tipos = Monstro.objects.values_list('tipo', flat=True).distinct().order_by('tipo')
        tamanhos = Monstro.objects.values_list('tamanho', flat=True).distinct().order_by('tamanho')
        crs = Monstro.objects.values_list('cr', flat=True).distinct().order_by('cr')
        sources = Monstro.objects.values_list('source', flat=True).distinct().order_by('source')
        acs = sorted(set(Monstro.objects.values_list('ac', flat=True).filter(ac__isnull=False)))
        
        return Response({
            'tipos': [t for t in tipos if t],
            'tamanhos': [t for t in tamanhos if t],
            'challenge_ratings': [c for c in crs if c],
            'sources': [s for s in sources if s],
            'armor_classes': acs,
        })

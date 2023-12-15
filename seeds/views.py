from rest_framework import generics
from .serializers import GrowingInfoSerializer,SeedSerializer
from .models import Seeds, GrowingInfo
from .filters import SeedFilters

# Create your views here.

class CreateGrowingInfoView(generics.CreateAPIView):
    serializer_class = GrowingInfoSerializer

class GrowingInfoUpdateView(generics.UpdateAPIView):
    serializer_class = GrowingInfoSerializer
    queryset = GrowingInfo.objects.all()
    lookup_field = "pk"
    
class RetriveGrowingOwnInfo(generics.RetrieveAPIView):    
    serializer_class = GrowingInfoSerializer
    queryset = GrowingInfo.objects.all()
    lookup_field = 'pk'

class CreateSeedInfoView(generics.CreateAPIView):
    serializer_class = SeedSerializer

class SeedUpdateView(generics.UpdateAPIView):
    serializer_class = SeedSerializer
    queryset = Seeds.objects.all()
    lookup_field = "pk"
    
class RetriveSeedOwnInfo(generics.RetrieveAPIView):    
    serializer_class = SeedSerializer
    queryset = Seeds.objects.all()
    lookup_field = 'pk'

class SeedListAPIView(generics.ListAPIView):
    serializer_class = SeedSerializer
    queryset = Seeds.objects.all()
    filterset_class = SeedFilters

from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .serializers import AssetSerializer
from .models import Asset

# Create your views here.
class ListAssetsAPIView(ListAPIView):
    queryset = Asset.objects.filter(is_public=True)
    serializer_class = AssetSerializer

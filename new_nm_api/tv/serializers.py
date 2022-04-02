from urllib.parse import urljoin
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.conf import settings
from .models import Asset, AssetType

class AssetTypeSerializer(ModelSerializer):
    class Meta:
        model = AssetType
        fields = '__all__'

class AssetSerializer(ModelSerializer):
    asset_type = AssetTypeSerializer()
    thumbnail_url = SerializerMethodField()
    file_url = SerializerMethodField()

    class Meta:
        model = Asset
        exclude = ('is_public', 'thumbnail', 'file')

    def get_thumbnail_url(self, obj):
        request = self.context['view'].request
        return urljoin('{scheme}://{host}{path}'.format(scheme=request.scheme,
                                                    host=request.get_host(),
                                                    path=settings.MEDIA_URL), 
                                                    obj.thumbnail.url)
        
    def get_file_url(self, obj):
        request = self.context['view'].request
        return urljoin('{scheme}://{host}{path}'.format(scheme=request.scheme,
                                                    host=request.get_host(),
                                                    path=settings.MEDIA_URL), 
                                                    obj.file.url)

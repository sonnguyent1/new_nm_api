import json
from urllib.parse import urlencode, urljoin
from urllib.request import urlopen, Request
from rest_framework.serializers import ModelSerializer, SerializerMethodField, \
    CharField, ListField, ValidationError, URLField, IntegerField
from django.conf import settings
from django.db import transaction
from django.contrib.auth.models import User
from new_nm_api.models.accounts import UserProfile

from new_nm_api.api.serializers.tv_presentation import UserSerializer
from .models import Asset, AssetType, Template, Class

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
class ClassModelSerializer(ModelSerializer):
    class Meta:
        model = Class 
        fields = '__all__'

class TemplateSerializer(ModelSerializer):
    owner_obj = SerializerMethodField()
    classes_to_share_obj = SerializerMethodField()
    owner = CharField(write_only=True,read_only=False, required=True)
    classes_to_share = ListField(child = IntegerField(), 
        write_only=True, read_only=False, required=False)
    displayed_image = URLField(required=True)
    class Meta:
        extra_kwargs = {
            'folder_id': {'required': False, 'allow_blank': True},
        } 
        model = Template
        fields = (
            'id',
            'code',
            'title',
            'folder_id',
            'description',
            'video_type',
            'displayed_image',
            'owner',
            'owner_obj',
            'is_deleted',
            'classes_to_share',
            'classes_to_share_obj',
            'allowed_functions',
        )


    def validate_owner(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise  ValidationError("User does not exist.")
        return user

    def validate_classes_to_share(self, value):
        valid = []
        for id in value:
            try:
                cl = Class.objects.get(pk=id)
            except Class.DoesNotExist:
                raise  ValidationError("Class does not exist.")
            valid.append(cl)
        return valid

    def get_owner_obj(self, obj):
        return (UserSerializer(obj.owner)).data 
    
    def get_classes_to_share_obj(self, obj):
        return [(ClassModelSerializer(cl)).data for cl in obj.classes_to_share.filter()]

    @transaction.atomic
    def save(self, **kwargs):
        classes = self.validated_data.pop('classes_to_share') if self.validated_data.get('classes_to_share') else None
        is_created = self.instance is None
        instance = super().save(**kwargs)
        if len(classes):
            if (instance.classes_to_share.count() > 0) :
                instance.classes_to_share.clear()
            instance.classes_to_share.add(*classes)
        
        if is_created:
            instance.folder_id = self.create_folder_for_user(instance)
        elif self.validated_data.get('folder_id'):
            instance.folder_id = self.validated_data['folder_id']
        
        instance.save()
        return instance

    def create_folder_for_user(self, obj):
        user = self.context['view'].request.user
        profile = UserProfile.objects.get(user_id=user.id)
        endpoint = profile.get_file_server()
        url = '%s/folders/create' % endpoint

        values = {
            'user_id': str(user.id),
            'app_secret': settings.FS_SECRET_KEY,
            'folder_name': obj.title,
            'usr': user.username
        }
        data = urlencode(values)
        req = Request(url, data.encode('utf-8'))
        creation_response = urlopen(req)
        json_str = creation_response.read()
        creation_dict = json.loads(json_str)
        if creation_dict.get('status') and creation_dict.get('status') == 'ok':
            return creation_dict.get('GUID')
        return None

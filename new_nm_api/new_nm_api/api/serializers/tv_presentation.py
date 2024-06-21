import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from django.conf import settings
from django.db import transaction
from django.db.models.query_utils import RegisterLookupMixin
from rest_framework import serializers
from ...models.tv_presentation import TVPresentation, TVPresentationMember
from ...models.accounts import UserProfile
from django.contrib.auth.models import User
from new_nm_api.settings import FileServers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_name', 'first_name')

class TVPresentationSerializer(serializers.ModelSerializer):
    user_obj = serializers.SerializerMethodField()
    member_objs = serializers.SerializerMethodField()
    user = serializers.CharField(write_only=True,read_only=False, required=True)
    members = serializers.ListField(child = serializers.CharField(), 
        write_only=True, read_only=False, required=False)
    class Meta:
        extra_kwargs = {
            'folder_id': {'required': False, 'allow_blank': True},
            'description': {'required': False, 'allow_blank': True},
        } 
        model = TVPresentation
        fields = (
            'id',
            'title',
            'folder_id',
            'description',
            'video_type',
            'display_color',
            'user',
            'user_obj',
            'member_objs',
            'duration',
            'file_size',
            'deleted',
            'template',
            # 'is_template',
            'members',
            'created_on',
            'last_modified'
        )


    def validate_user(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise  serializers.ValidationError("User does not exist.")
        return user

    def validate_members(self, value):
        valid = []
        for id in value:
            try:
                user = User.objects.get(username=id)
            except User.DoesNotExist:
                raise  serializers.ValidationError("User does not exist.")
            valid.append(user)
        return valid

    def get_user_obj(self, obj):
        return (UserSerializer(obj.user)).data 
    
    def get_member_objs(self, obj):
        return [(UserSerializer(m.user)).data for m in obj.members.filter(user__is_active=True)]
    
    def update_folder_permission_for_user(self, is_share, user_id):
        try:
            url = '%s/folders/%s/%s' % (FileServers.DEFAULTS, self.instance.folder_id, 'share' if is_share else 'unshare')
            print('[update_folder_permission_for_user] URL: %s' % url)
            params = {
                'with_user': user_id,
                'app_secret': settings.FS_SECRET_KEY,
                'user_id': self.instance.user_id,
            }
            data = urlencode(params)
            req = Request(url, data.encode('utf-8'))
            response = urlopen(req)
            json_str = response.read()
            json_dict = json.loads(json_str)
            if json_dict.get('status') and json_dict.get('status') == 'ok':
                print('Folder shared with user %s' % user_id)
                return True
        except Exception as e:
            print('[update_folder_permission_for_user] Error: %s' % str(e))
        return False

    @transaction.atomic
    def save(self, **kwargs):
        members = self.validated_data.pop('members') if self.validated_data.get('members') else None
        is_created = self.instance is None
        instance = super().save(**kwargs)
        if members is not None:
            existing_members = TVPresentationMember.objects.filter(tvpresentation_id=instance.pk)
            if existing_members is not None and existing_members.count() > 0:
                for existing_member in existing_members:
                    self.update_folder_permission_for_user(False, existing_member.user_id)
                existing_members.delete()

            qs_members = User.objects.filter(pk__in=[user.id for user in members])
            if qs_members.count() == len(members):
                for m in members:
                    TVPresentationMember.objects.update_or_create(tvpresentation_id=instance.pk, user_id=m.id)
                    self.update_folder_permission_for_user(True, m.id)
        
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

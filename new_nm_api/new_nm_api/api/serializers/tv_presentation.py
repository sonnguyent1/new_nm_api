from rest_framework import serializers
from ...models.tv_presentation import TVPresentation, TVPresentationMember
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_name', 'first_name')

class TVPresentationSerializer(serializers.ModelSerializer):
    user_obj = serializers.SerializerMethodField()
    member_objs = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(write_only=True, 
        queryset=User.objects
        # .none()
        .filter(is_active=True, is_superuser=False))
    members = serializers.ListField(child = serializers.IntegerField(), 
        write_only=True, read_only=False, required=False)
    class Meta:
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
            'is_template',
            'members'
        )

    def get_user_obj(self, obj):
        return (UserSerializer(obj.user)).data 
    
    def get_member_objs(self, obj):
        return [(UserSerializer(m.user)).data for m in obj.members.filter(user__is_active=True, user__is_superuser=False)]

    def save(self, **kwargs):
        members = self.validated_data.pop('members') if self.validated_data.get('members') else None
        instance = super().save(**kwargs)
        if members:
            qs_members = User.objects.filter(pk__in=members)
            if qs_members.count() == len(members):
                for m in members:
                    TVPresentationMember.objects.update_or_create(tvpresentation_id=instance.pk, user_id=m)
        return instance
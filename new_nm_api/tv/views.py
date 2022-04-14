from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from django.db.models import Q


from .serializers import AssetSerializer, TemplateSerializer
from .models import Asset, ClassMembers, Template

# Create your views here.
class ListAssetsAPIView(ListAPIView):
    queryset = Asset.objects.filter(is_public=True)
    serializer_class = AssetSerializer



class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.filter(is_deleted=False)
    serializer_class = TemplateSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner_id=self.request.user.pk)


templates_details = TemplateViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

templates = TemplateViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

class UsableTemplateListAPIView(ListAPIView):
    queryset = TemplateViewSet.queryset
    serializer_class = TemplateViewSet.serializer_class

    def get_queryset(self):
        qs = super().get_queryset()
        class_ids = list(ClassMembers.objects.filter(user_id=self.request.user.pk).values_list('class_id', flat=True))
        return qs.filter(Q(classes_to_share__pk__in=class_ids) | Q(owner=self.request.user))

usable_templates = UsableTemplateListAPIView.as_view()

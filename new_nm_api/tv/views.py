from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from django.db.models import Q
from datetime import date


from .serializers import AssetSerializer, TemplateSerializer
from .models import Asset, ClassMembers, Sale, Template

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
        user = self.request.user
        class_ids = list(ClassMembers.objects.filter(user_id=user.pk).values_list('class_id', flat=True))
        ids = qs.filter(Q(classes_to_share__pk__in=class_ids) | Q(owner=user)).values_list('id', flat=True)

        sale_user_ids = [user.id,] 
        try:
            sale_user_ids.append(user.userprofile.group_account_id)
        except:
            pass

        today = date.today()
        sale_template_ids = list(Sale.objects.filter(user_id__in=sale_user_ids,
            is_activated=True, expired_date__gt=today)
            .values_list('templates__template__pk', flat=True))
       
        return qs.filter(Q(pk__in=ids) | Q(pk__in=sale_template_ids))

usable_templates = UsableTemplateListAPIView.as_view()

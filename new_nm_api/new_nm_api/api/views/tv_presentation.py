
from rest_framework import viewsets
from django.db import transaction
from ..serializers.tv_presentation import TVPresentationSerializer
from ...models.tv_presentation import TVPresentation, TVPresentationMember


class TVPresentationViewSet(viewsets.ModelViewSet):
    queryset = TVPresentation.objects.filter(deleted=False)
    serializer_class = TVPresentationSerializer

    @transaction.atomic
    def perform_destroy(self, instance):
        TVPresentationMember.objects.filter(tvpresentation_id=instance.pk).delete()
        super().perform_destroy(instance)



presentations_details = TVPresentationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

presentations = TVPresentationViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
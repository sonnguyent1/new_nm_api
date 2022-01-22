
from rest_framework import viewsets
from django.db import transaction
from django.db.models import Q
from ..serializers.tv_presentation import TVPresentationSerializer
from ...models.tv_presentation import TVPresentation, TVPresentationMember


class TVPresentationViewSet(viewsets.ModelViewSet):
    queryset = TVPresentation.objects.filter(deleted=False)
    serializer_class = TVPresentationSerializer

    @transaction.atomic
    def perform_destroy(self, instance):
        TVPresentationMember.objects.filter(
            tvpresentation_id=instance.pk).delete()
        super().perform_destroy(instance)

    def get_queryset(self):
        qs = super().get_queryset()
        members = TVPresentationMember.objects.filter(
            user_id=self.request.user.pk)
        return qs.filter(Q(user_id=self.request.user.pk) | Q(user_id=self.request.user.pk) | Q(pk__in=[m.tvpresentation_id for m in members]))


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

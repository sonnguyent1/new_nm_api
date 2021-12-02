
from rest_framework import viewsets
from ..serializers.tv_presentation import TVPresentationSerializer
from ...models.tv_presentation import TVPresentation


class TVPresentationViewSet(viewsets.ModelViewSet):
    queryset = TVPresentation.objects.filter(deleted=False)
    serializer_class = TVPresentationSerializer


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
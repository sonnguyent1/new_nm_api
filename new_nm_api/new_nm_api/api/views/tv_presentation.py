
from rest_framework import viewsets
from django.db import transaction
from django.db.models import Q
from ..serializers.tv_presentation import TVPresentationSerializer
from ...models.tv_presentation import TVPresentation, TVPresentationMember
from rest_framework.response import Response
from rest_framework import status


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

def share_folder_presentation_members(request, pk=None):
    if request.method == 'POST':
        try:
            presentation = TVPresentation.objects.get(pk=pk)
            serializer = TVPresentationSerializer(presentation)
            for member in presentation.members.all():
                result = serializer.update_folder_permission_for_user(True, member.user_id)
                if not result:
                    return Response({'status': 'error', 'message': 'Error sharing folder with members.'}, status=status.HTTP_400_BAD_REQUEST)
            # responde list of members in json 
            return Response(list(presentation.members.values_list('user_id', flat=True)), status=status.HTTP_200_OK)
        except TVPresentation.DoesNotExist:
            return Response({'status': 'error', 'message': 'Presentation does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'status': 'error', 'message': 'Method not allowed.'}, status=status.HTTP_400_BAD_REQUEST)


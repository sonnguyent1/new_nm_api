from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q
from datetime import date, datetime, timedelta
from pytz import utc
from new_nm_api.api.serializers.tv_presentation import TVPresentationSerializer

from .serializers import AssetSerializer, TemplateSerializer
from .models import Asset, ClassMembers, Sale, Template, PublishQueue

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
    
@api_view(['GET'])
def get_publish_queues(request):
    # Get all rows in PublishQueue where Completed = false and (Date Processed = null or Date Processed > 1 hour behind the current time), ordered by Date Added ascending
    current_datetime = datetime.now(utc)
    one_hour_ago = current_datetime - timedelta(hours=1)
    publish_queue_qs = PublishQueue.objects.filter(is_completed=False).filter(
        Q(date_processed=None) | Q(date_processed__lt=one_hour_ago)).order_by('date_added')
    
    return Response([{
        'id': pq.id,
        'presentation_id': pq.presentation_id,
        'date_added': pq.date_added,
        'date_processed': pq.date_processed,
        'is_completed': pq.is_completed,
    } for pq in publish_queue_qs], status=status.HTTP_200_OK)

@api_view(['POST'])
def publish_queue_dequeue(request, pk=None):
    # Get the row in PublishQueue with the given ID
    try:
        publish_queue = PublishQueue.objects.get(pk=pk)
    except PublishQueue.DoesNotExist:
        return Response({'status': 'error', 'message': 'PublishQueue does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Set the Date Processed to the current time
    publish_queue.date_processed = datetime.now(utc)
    publish_queue.save()

    response_data = {'status': 'success', 'message': 'PublishQueue processed.'}

    if (publish_queue.presentation is not None):
        algorithm, salt, hsh = publish_queue.presentation.user.password.split('$')
        username = publish_queue.presentation.user.username
        response_data['usr'] = username
        response_data['pwd'] = hsh
        serializer = TVPresentationSerializer(publish_queue.presentation)
        response_data['presentation'] = serializer.data
    
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def publish_queue_complete(request, pk=None):
    # Get the row in PublishQueue with the given ID
    try:
        publish_queue = PublishQueue.objects.get(pk=pk)
    except PublishQueue.DoesNotExist:
        return Response({'status': 'error', 'message': 'PublishQueue does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Set the Is Completed to true
    publish_queue.is_completed = True
    publish_queue.save()
    
    return Response({'status': 'success', 'message': 'PublishQueue completed.'}, status=status.HTTP_200_OK)


usable_templates = UsableTemplateListAPIView.as_view()

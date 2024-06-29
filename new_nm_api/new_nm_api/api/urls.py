from django.urls.conf import re_path
from .views.tv_presentation import presentations_details, presentations, share_folder_presentation_members, publish_presentation

urlpatterns = [ 
    re_path('^$', presentations),
    re_path('^(?P<pk>\d+)/?$', presentations_details),
    re_path('^(?P<pk>\d+)/sharefolder/?$', share_folder_presentation_members),
    re_path('^(?P<pk>\d+)/publish/?$', publish_presentation),
]
from django.urls.conf import re_path
from .views.tv_presentation import presentations_details, presentations

urlpatterns = [ 
    re_path('^$', presentations),
    re_path('^(?P<pk>\d+)/?$', presentations_details),
]
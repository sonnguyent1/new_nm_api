from django.urls.conf import re_path
from .views import ListAssetsAPIView, templates, templates_details, usable_templates

urlpatterns = [ 
    re_path('^assets/?$', ListAssetsAPIView.as_view()),
    re_path('^templates/?$', templates),
    re_path('^templates/usable/?$', usable_templates),
    re_path('^templates/(?P<pk>\d+)/?$', templates_details),
]
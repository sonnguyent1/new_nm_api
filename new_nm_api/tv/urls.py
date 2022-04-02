from django.urls.conf import re_path
from .views import ListAssetsAPIView

urlpatterns = [ 
    re_path('^assets/?$', ListAssetsAPIView.as_view()),
]
from typing import Callable
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class TVPresentation(models.Model):
    title = models.CharField(max_length=255)
    folder_id = models.CharField(max_length=127)
    description = models.TextField()
    video_type = models.CharField(max_length=16, 
        choices=(('tall', 'TALL'), ('wide', 'WIDE',),))
    display_color = models.CharField(max_length=32)
    user = models.ForeignKey(User, related_name='presentation', on_delete=models.CASCADE)
    # members = models.ManyToManyField(User, blank=True, db_table='nm_projects_tvpresentation_members')
    duration = models.PositiveIntegerField()
    file_size = models.PositiveIntegerField()
    deleted = models.BooleanField(default=False)
    template = models.CharField(max_length=127, null=True)
    is_template = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'nm_projects_tvpresentation'
        app_label = 'new_nm_api'

class TVPresentationMember(models.Model):
    tvpresentation = models.ForeignKey(TVPresentation, on_delete=CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=CASCADE)

    class Meta:
        db_table = 'nm_projects_tvpresentation_members'
        app_label = 'new_nm_api'
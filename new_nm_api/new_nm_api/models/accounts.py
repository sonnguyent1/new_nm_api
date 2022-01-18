from django.db import models
from django.contrib.auth.models import User
from new_nm_api.settings import FileServers


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    country = models.CharField(max_length=50, default='', blank=True)

    class Meta:
        db_table = 'accounts_userprofile'
        managed=False
        app_label = 'new_nm_api'

    def get_file_server(self):
        if (self.country == 'China'):
            return FileServers.CHINA
        elif self.country in ['United States', 'Canada', 'Netherlands']:
            return FileServers.WESTERN
        return FileServers.DEFAULTS
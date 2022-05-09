from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models import deletion

# Create your models here.
class AssetLanguage(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class AssetType(models.Model):
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=127)

    def __str__(self):
        return self.name

class Asset(models.Model):
    asset_type = models.ForeignKey(AssetType, on_delete=models.deletion.CASCADE)
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='nm_tv_assets_thumbs')
    file = models.FileField(upload_to='nm_tv_assets_files')
    is_public= models.NullBooleanField()

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length = 255)
    
    class Meta:
        db_table = 'schools_class'

class ClassMembers(models.Model):
    class_id = models.IntegerField()
    user_id = models.IntegerField()
    class Meta:
        db_table = 'schools_class_members'

class Template(models.Model):
    code = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    folder_id = models.CharField(max_length=127)
    description = models.TextField(blank=True, null=True)
    video_type = models.CharField(max_length=16, 
        choices=(('tall', 'TALL'), ('wide', 'WIDE',),))
    owner = models.ForeignKey(User, on_delete=deletion.CASCADE)
    is_deleted = models.BooleanField(default=False)
    classes_to_share = models.ManyToManyField(Class, blank=True)
    allowed_functions = models.TextField(blank=True, null=True)
    displayed_image = models.CharField(max_length=1024, null=True, blank=True)
    created_on = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

class TemplateForSale(models.Model):
    template = models.ForeignKey(Template, blank=True, null=True, on_delete=models.SET_NULL)
    language = models.ForeignKey(AssetLanguage, blank=True, null=True, on_delete=models.SET_NULL)
    is_public = models.BooleanField(default=False)
    keywords = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

class Sale(models.Model):
    creator = models.ForeignKey(User, on_delete=models.deletion.SET_NULL, null=True, related_name='created_sales')
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE, related_name='sales', unique=True)
    is_activated = models.BooleanField(default=True)
    expired_date = models.DateField(null=True, blank=True)
    additional_assets = models.ManyToManyField(Asset)
    allow_online_saving = models.NullBooleanField(default=False)
    allow_upload_to_NM = models.NullBooleanField(default=False)
    allow_template = models.NullBooleanField(default=False)
    allow_access_to_asset_store = models.NullBooleanField(default=False)
    templates = models.ManyToManyField(TemplateForSale, blank=True, null=True)

    def __str__(self):
        return ' '.join((self.user.first_name, self.user.last_name,))


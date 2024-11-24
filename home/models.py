import uuid

from django_ckeditor_5.fields import CKEditor5Field
from django.db import models


class UploadModel(models.Model):
    input_video = models.FileField(upload_to="file/vidoe/")
    mime_type = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, blank=True, null=True, default="Processing")
    audio_url = models.FileField(upload_to="file/audio/", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_url = models.CharField(max_length=100, default=uuid.uuid4)




    def __str__(self) -> str:
        return f"{self.input_video} | {self.uploaded_at}" 




class BlogModel(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True)
    text = CKEditor5Field()
    picture_load = models.FileField(upload_to="file/thumb", null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title 



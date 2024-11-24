# celery tasks
import mimetypes
import os
from datetime import datetime, timedelta

import pytz
from assistant.movie import extract_audio
from celery import shared_task
from django.conf import settings

from .models import UploadModel


@shared_task(ignore_result=True)
def proccessing_to_convert_video(file_id):
    get_task = None
    try:
        get_task = UploadModel.objects.get(pk=file_id)
    except:
        pass
    if get_task:
        file_path = get_task.input_video.path
        filename, _ = os.path.splitext(os.path.basename(file_path)) 

        get_task.audio_url.name = f"file/audio/{filename}.mp3"
        if settings.DEBUG:
            audio_path = os.path.join(settings.BASE_DIR, "media", "file", "audio")
            if not os.path.isdir(audio_path):
                os.mkdir(audio_path)
            export_path = os.path.join(settings.BASE_DIR, "media", "file", "audio", f"{filename}.mp3")
        else:
            audio_path = os.path.join("/", "var", "log", "extract_audio", "media", "file", "audio")
            if not os.path.isdir(audio_path):
                os.mkdir(audio_path)
            export_path = os.path.join("/", "var", "log","extract_audio", "media", "file", "audio", f"{filename}.mp3") 
        get_response = extract_audio(file_path, export_path)
        mime_type, _ = mimetypes.guess_type(export_path)
        get_task.mime_type = mime_type


        if get_response:
            get_task.status = "Success"
        else:
            get_task.status = "Failed"
        get_task.save()



@shared_task
def remove_expired_urls():
    video_path = os.path.join(settings.MEDIA_ROOT, "file", "vidoe")
    audio_path = os.path.join(settings.MEDIA_ROOT, "file", "audio")

    list_all_video = os.listdir(video_path)
    time_threshold = datetime.now(pytz.timezone(settings.TIME_ZONE)) - timedelta(hours=24)

    for any_video in list_all_video:
        try:
            item_task = UploadModel.objects.get(uploaded_at__lt=time_threshold, input_video=f"file/vidoe/{any_video}")
        except:
            continue

        if item_task:
            try:
                os.remove(os.path.join(video_path, any_video))
            except:
                pass
            try:
                file_path = item_task.input_video.path
                filename, _ = os.path.splitext(os.path.basename(file_path)) 
                os.remove(os.path.join(audio_path, f"{filename}.mp3"))
            except:
                pass
            item_task.delete()

    UploadModel.objects.filter(uploaded_at__lt=time_threshold).delete()





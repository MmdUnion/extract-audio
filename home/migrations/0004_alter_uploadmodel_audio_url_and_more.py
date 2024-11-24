# Generated by Django 4.1.4 on 2023-01-04 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_uploadmodel_audio_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmodel',
            name='audio_url',
            field=models.FileField(blank=True, null=True, upload_to='file/audio/'),
        ),
        migrations.AlterField(
            model_name='uploadmodel',
            name='input_video',
            field=models.FileField(upload_to='file/vidoe/'),
        ),
    ]

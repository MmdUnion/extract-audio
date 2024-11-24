# Generated by Django 4.1.5 on 2023-01-15 18:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_uploadmodel_mime_type_alter_uploadmodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadmodel',
            name='download_url',
            field=models.CharField(default=uuid.uuid4, max_length=100),
        ),
    ]

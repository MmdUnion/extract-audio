# Generated by Django 4.1.7 on 2023-06-04 15:02

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_blogmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogmodel',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]

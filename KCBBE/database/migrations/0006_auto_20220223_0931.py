# Generated by Django 3.2.12 on 2022-02-23 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='docfile',
        ),
        migrations.AddField(
            model_name='document',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='document',
            name='document',
            field=models.FileField(blank=True, upload_to='documents/'),
        ),
    ]

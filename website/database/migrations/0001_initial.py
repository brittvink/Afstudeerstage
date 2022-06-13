# Generated by Django 3.2.12 on 2022-03-10 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('link', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=1000)),
                ('published', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('search_id', models.CharField(max_length=100)),
                ('article_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vocabulair',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('key_id', models.CharField(max_length=100)),
                ('word', models.CharField(max_length=100)),
            ],
        ),
    ]
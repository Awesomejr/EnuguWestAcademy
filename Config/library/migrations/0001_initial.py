# Generated by Django 5.1.2 on 2024-11-02 14:17

import django.db.models.deletion
import library.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('file', models.FileField(max_length=300, upload_to=library.models.eBookPath)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=library.models.eBookThumbnailPath)),
                ('is_public', models.BooleanField(default=False)),
                ('assigned_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.classname')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.subject')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.category')),
            ],
            options={
                'verbose_name_plural': 'Books',
            },
        ),
    ]

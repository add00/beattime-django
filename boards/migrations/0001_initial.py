# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import boards.fields.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation_date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='creation_date')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('sequence', models.PositiveIntegerField()),
                ('author', models.ForeignKey(verbose_name='author', to='profiles.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation_date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='creation_date')),
                ('object_id', models.PositiveIntegerField()),
                ('author', models.ForeignKey(verbose_name='author', to='profiles.Profile')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Desk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desk_slug', models.SlugField(unique=True, max_length=5)),
                ('owner', models.OneToOneField(verbose_name='owner', to='profiles.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', boards.fields.models.RGBField(verbose_name='color')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Sticker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation_date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='creation_date')),
                ('caption', models.CharField(max_length=100, verbose_name='caption')),
                ('description', models.TextField(verbose_name='description')),
                ('status', models.CharField(max_length=1, verbose_name='status', choices=[('O', 'OPEN'), ('I', 'IN PROGRESS'), ('R', 'REVIEW'), ('D', 'DONE'), ('B', 'BLOCKED')])),
                ('author', models.ForeignKey(verbose_name='author', to='profiles.Profile')),
                ('board', models.ForeignKey(verbose_name='board', to='boards.Board')),
                ('label', models.ForeignKey(verbose_name='label', to='boards.Label')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='board',
            name='desk',
            field=models.ForeignKey(verbose_name='desk', to='boards.Desk'),
        ),
        migrations.AlterUniqueTogether(
            name='board',
            unique_together=set([('desk', 'sequence')]),
        ),
    ]

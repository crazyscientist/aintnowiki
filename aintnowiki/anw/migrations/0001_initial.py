# Generated by Django 2.0.6 on 2018-06-17 13:24

from django.db import migrations, models
import django.db.models.deletion
import tagging.fields
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Timestamp - created')),
                ('changed', models.DateTimeField(auto_now=True, help_text='Timestamp - last changed')),
                ('title', models.CharField(help_text='Title of the Page', max_length=75)),
                ('title_slug', models.SlugField(help_text='Slug used in URL', unique=True)),
                ('body', tinymce.models.HTMLField(help_text='Content of the Page')),
                ('featured', models.BooleanField(help_text='Should it appear on the navigation/side bar?')),
                ('tags', tagging.fields.TagField(blank=True, help_text='List of Tags', max_length=255)),
                ('meta_keywords', models.TextField(blank=True, help_text='Keywords for meta tag.', null=True)),
                ('meta_description', models.TextField(blank=True, help_text='Description for meta tag and children listing.', null=True)),
                ('parent', models.ForeignKey(blank=True, help_text='Parent Page', null=True, on_delete=django.db.models.deletion.PROTECT, to='anw.Page')),
            ],
        ),
    ]
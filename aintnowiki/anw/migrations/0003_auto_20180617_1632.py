# Generated by Django 2.0.6 on 2018-06-17 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anw', '0002_auto_20180617_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='footer',
            field=models.BooleanField(default=False, help_text='Should it appear in the footer?'),
        ),
        migrations.AlterField(
            model_name='page',
            name='featured',
            field=models.BooleanField(default=False, help_text='Should it appear on the navigation bar?'),
        ),
    ]

# Generated by Django 4.2.3 on 2023-08-30 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib_app', '0002_returnedmodal_delete_returnmodal'),
    ]

    operations = [
        migrations.AddField(
            model_name='renthistorymodaltesting',
            name='is_lost',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rentmodal',
            name='is_lost',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='returnedmodal',
            name='is_lost',
            field=models.BooleanField(default=False),
        ),
    ]

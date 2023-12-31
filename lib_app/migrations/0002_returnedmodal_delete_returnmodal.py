# Generated by Django 4.2.3 on 2023-08-17 09:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lib_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnedModal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fine', models.CharField(max_length=250)),
                ('Return_date', models.DateField(blank=True, null=True)),
                ('is_returned', models.BooleanField(default=False)),
                ('Rent_Book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lib_app.bookmodal')),
                ('Rent_details', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lib_app.rentmodal')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='ReturnModal',
        ),
    ]

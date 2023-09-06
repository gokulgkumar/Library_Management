# Generated by Django 4.2.3 on 2023-08-30 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lib_app', '0003_renthistorymodaltesting_is_lost_rentmodal_is_lost_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersModal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Price', models.CharField(max_length=250)),
                ('Order_date', models.DateField(blank=True, null=True)),
                ('Book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lib_app.bookmodal')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lib_app.ordermodal')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

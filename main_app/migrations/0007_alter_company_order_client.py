# Generated by Django 4.1.3 on 2023-03-23 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_company_order_company_process'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_order',
            name='Client',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main_app.company_client'),
            preserve_default=False,
        ),
    ]
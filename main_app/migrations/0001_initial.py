# Generated by Django 4.1.3 on 2023-03-05 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=45)),
                ('Description', models.CharField(max_length=250)),
                ('membership', models.BooleanField(default=False)),
                ('Creation_date', models.DateTimeField()),
                ('Last_membership_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Company_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_Received', models.DateTimeField()),
                ('Description', models.CharField(max_length=150)),
                ('Status', models.CharField(max_length=10)),
                ('Client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company')),
            ],
        ),
        migrations.CreateModel(
            name='Company_Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Process_Name', models.CharField(max_length=20)),
                ('Description', models.CharField(max_length=150)),
                ('Company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company')),
            ],
        ),
        migrations.CreateModel(
            name='Company_Process_step_template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Step_Name', models.CharField(max_length=20)),
                ('Step_Order_Number', models.IntegerField()),
                ('Description', models.CharField(max_length=150)),
                ('Company_Process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company_process')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_key', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('user_email', models.CharField(max_length=40)),
                ('creation_date', models.DateTimeField()),
                ('expire_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.CharField(max_length=40, unique=True)),
                ('Username', models.CharField(max_length=40)),
                ('Password', models.CharField(max_length=200)),
                ('Name', models.CharField(max_length=40)),
                ('Birthdate', models.DateField()),
                ('User_Since', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Process_Step_Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Notes', models.CharField(max_length=100, null=True)),
                ('Status', models.CharField(max_length=10)),
                ('Company_Process_step_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company_process_step_template')),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company_order')),
            ],
        ),
        migrations.CreateModel(
            name='Mapping_Usuario_Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Level', models.CharField(max_length=10)),
                ('Company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

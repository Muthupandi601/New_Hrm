# Generated by Django 3.2.8 on 2021-11-02 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Client_Name', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'client_table',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('Unit_Name', models.CharField(max_length=200)),
                ('Client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Unit', to='hrm.client')),
            ],
            options={
                'db_table': 'unit_table',
            },
        ),
    ]

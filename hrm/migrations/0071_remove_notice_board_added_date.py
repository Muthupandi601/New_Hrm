# Generated by Django 3.2.9 on 2022-06-24 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0070_notice_board'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice_board',
            name='ADDED_DATE',
        ),
    ]

# Generated by Django 3.2.8 on 2022-02-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0017_auto_20220221_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary_details',
            name='ESIC',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='salary_details',
            name='PF',
            field=models.CharField(default='', max_length=150),
        ),
    ]

# Generated by Django 3.2.9 on 2022-05-23 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0046_emp_advance_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp_advance_details',
            name='GIVEN_AMOUNT',
            field=models.CharField(default='', max_length=100),
        ),
    ]

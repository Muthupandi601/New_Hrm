# Generated by Django 3.2.9 on 2022-05-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0047_emp_advance_details_given_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp_advance_details',
            name='GIVING_AMOUNT',
            field=models.CharField(default='', max_length=100),
        ),
    ]

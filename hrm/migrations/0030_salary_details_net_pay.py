# Generated by Django 3.2.9 on 2022-04-08 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0029_salary_details_total_deducation'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary_details',
            name='NET_PAY',
            field=models.CharField(default='', max_length=150),
        ),
    ]

# Generated by Django 3.2.9 on 2022-06-15 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0065_emp_certificate_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave_category_list',
            name='IMAGE',
            field=models.CharField(default='', max_length=150),
        ),
    ]

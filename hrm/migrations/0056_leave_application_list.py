# Generated by Django 3.2.9 on 2022-06-04 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0055_leave_category_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='LEAVE_APPLICATION_LIST',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('EMP_CODE', models.CharField(default='', max_length=120)),
                ('EMP_NAME', models.CharField(default='', max_length=150)),
                ('DESIGNATION', models.CharField(default='', max_length=150)),
                ('REASON', models.CharField(default='', max_length=150)),
                ('START_DATE', models.CharField(default='', max_length=150)),
                ('END_DATE', models.CharField(default='', max_length=150)),
                ('LEAVE_CATEGORY', models.CharField(default='', max_length=150)),
                ('LEAVE_DAYS', models.CharField(default='', max_length=150)),
                ('STATUS', models.CharField(default='', max_length=150)),
                ('ADDED_DATE', models.CharField(default='', max_length=150)),
                ('TIMESTAMP', models.DateTimeField(auto_now_add=True, max_length=50)),
            ],
            options={
                'db_table': 'leave_application_list',
            },
        ),
    ]

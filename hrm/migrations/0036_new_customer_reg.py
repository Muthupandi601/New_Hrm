# Generated by Django 3.2.9 on 2022-05-14 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0035_auto_20220514_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='New_Customer_Reg',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('CLIENT_CODE', models.CharField(max_length=50)),
                ('CLIENT_NAME', models.CharField(max_length=50)),
                ('EMAIL', models.CharField(default='', max_length=150)),
                ('DOB', models.CharField(default='', max_length=150)),
                ('CONTACT_NO', models.CharField(default='', max_length=50)),
                ('WEB', models.CharField(default='', max_length=25)),
                ('GENTER', models.CharField(default='', max_length=25)),
                ('EMERGENCY_CONTACT_NO', models.CharField(default='', max_length=50)),
                ('ADDRESS', models.CharField(default='', max_length=150)),
                ('REG_DATE', models.CharField(max_length=50)),
                ('REG_TIME', models.CharField(max_length=50)),
                ('CLIENT_TYPE', models.CharField(default='', max_length=150)),
                ('TIMESTAMP', models.DateTimeField(auto_now_add=True, max_length=50)),
            ],
            options={
                'db_table': 'customer_register',
            },
        ),
    ]

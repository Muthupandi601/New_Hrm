# Generated by Django 3.2.8 on 2021-11-07 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0002_client_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='monthly_attendance',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('EMP_CODE', models.CharField(max_length=50)),
                ('DAYS_PRESENT', models.IntegerField(max_length=11)),
                ('EXTRA_DUTIES', models.IntegerField(max_length=11)),
                ('WEEKLY_OFFS', models.IntegerField(max_length=11)),
                ('OT_HRS', models.IntegerField(max_length=11)),
                ('TOTAL_DAYS', models.IntegerField(max_length=11)),
                ('ABSENT', models.IntegerField(max_length=11)),
                ('DIVIDE_BY_DAYS', models.IntegerField(max_length=11)),
                ('BASIC_RATE', models.IntegerField(max_length=11)),
                ('INVENTORY', models.IntegerField(max_length=11)),
                ('ADVANCE', models.IntegerField(max_length=11)),
                ('PT', models.IntegerField(max_length=11)),
                ('TDS', models.IntegerField(max_length=11)),
                ('OTHER_DEDUCTION', models.IntegerField(max_length=11)),
                ('OTHER_DEDUCTION_DESCRIPTION', models.IntegerField(max_length=11)),
                ('TIMESTAMP', models.DateTimeField(auto_now_add=True, max_length=50)),
            ],
            options={
                'db_table': 'emp_monthly_attendance',
            },
        ),
    ]
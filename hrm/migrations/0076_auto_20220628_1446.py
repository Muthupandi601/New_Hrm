# Generated by Django 3.2.9 on 2022-06-28 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0075_alter_new_emp_reg_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='MANAGE_FILES',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('CAPTION', models.CharField(default='', max_length=120)),
                ('UPLOAD_FILE', models.CharField(default='', max_length=300)),
                ('CREATED_AT', models.CharField(default='', max_length=150)),
                ('TIMESTAMP', models.DateTimeField(auto_now_add=True, max_length=50)),
            ],
            options={
                'db_table': 'manage_files',
            },
        ),
        migrations.AlterField(
            model_name='new_emp_reg',
            name='DOB',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='new_emp_reg',
            name='EMP_CODE',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='new_emp_reg',
            name='EMP_NAME',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='new_emp_reg',
            name='GENDER',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='new_emp_reg',
            name='MOBILE_NO',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AlterField(
            model_name='new_emp_reg',
            name='REG_DATE',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='new_emp_reg',
            name='REG_TIME',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='new_emp_reg',
            name='SALUTATION',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='new_emp_reg',
            name='USER_TYPE',
            field=models.CharField(default='', max_length=25),
        ),
    ]

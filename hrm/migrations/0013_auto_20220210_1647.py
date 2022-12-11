# Generated by Django 3.2.8 on 2022-02-10 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0012_salary_details'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salary_details',
            options={'managed': True},
        ),
        migrations.AddField(
            model_name='emp_police_verfication',
            name='EMP_SAL',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='hrm.salary_details', verbose_name='emp_sal'),
        ),
        migrations.AddField(
            model_name='salary_details',
            name='EMP_LINK',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='hrm.emp_bank_details', verbose_name='emp_link'),
        ),
    ]

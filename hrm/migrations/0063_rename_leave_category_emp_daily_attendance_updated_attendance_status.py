# Generated by Django 3.2.9 on 2022-06-08 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0062_rename_leave_category_emp_daily_attendance_list_attendance_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emp_daily_attendance_updated',
            old_name='LEAVE_CATEGORY',
            new_name='ATTENDANCE_STATUS',
        ),
    ]

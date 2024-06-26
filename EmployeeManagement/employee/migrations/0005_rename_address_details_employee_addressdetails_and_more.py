# Generated by Django 5.0.3 on 2024-03-29 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_alter_employee_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='address_details',
            new_name='addressDetails',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='phone_no',
            new_name='phoneNo',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='work_experience',
            new_name='workExperience',
        ),
        migrations.RenameField(
            model_name='qualification',
            old_name='from_date',
            new_name='fromDate',
        ),
        migrations.RenameField(
            model_name='qualification',
            old_name='qualification_name',
            new_name='qualificationName',
        ),
        migrations.RenameField(
            model_name='qualification',
            old_name='to_date',
            new_name='toDate',
        ),
        migrations.RenameField(
            model_name='workexperience',
            old_name='company_name',
            new_name='companyName',
        ),
        migrations.RenameField(
            model_name='workexperience',
            old_name='from_date',
            new_name='fromDate',
        ),
        migrations.RenameField(
            model_name='workexperience',
            old_name='to_date',
            new_name='toDate',
        ),
    ]

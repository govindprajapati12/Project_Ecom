# Generated by Django 5.0.6 on 2024-06-25 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='comapany_address',
            new_name='company_address',
        ),
    ]
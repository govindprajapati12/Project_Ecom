# Generated by Django 5.0.6 on 2024-06-21 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='comapany_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(default='', upload_to='porfiles/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
    ]

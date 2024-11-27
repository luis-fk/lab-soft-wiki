# Generated by Django 5.1.1 on 2024-11-27 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0011_siteinfo_created_at_siteinfo_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('staff', 'Staff'), ('admin', 'Admin'), ('inactive', 'Inactive')], default='user', max_length=10),
        ),
    ]
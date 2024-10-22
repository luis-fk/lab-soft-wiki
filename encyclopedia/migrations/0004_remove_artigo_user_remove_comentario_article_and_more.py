# Generated by Django 5.1.1 on 2024-10-26 15:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0003_rename_cidade_user_city_alter_user_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artigo',
            name='user',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='article',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='user',
        ),
        migrations.AddField(
            model_name='artigo',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comentario',
            name='article_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comentario',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='comentario',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
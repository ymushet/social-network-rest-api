# Generated by Django 3.0.4 on 2020-03-26 15:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_edited'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'ordering': ('updated_at',)},
        ),
        migrations.AddField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='like',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

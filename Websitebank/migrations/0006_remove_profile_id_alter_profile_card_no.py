# Generated by Django 4.0.4 on 2022-06-01 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Websitebank', '0005_alter_profile_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id',
        ),
        migrations.AlterField(
            model_name='profile',
            name='card_no',
            field=models.CharField(max_length=16, primary_key=True, serialize=False, unique=True),
        ),
    ]

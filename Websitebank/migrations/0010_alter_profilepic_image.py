# Generated by Django 4.0.4 on 2022-06-05 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Websitebank', '0009_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepic',
            name='image',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
    ]
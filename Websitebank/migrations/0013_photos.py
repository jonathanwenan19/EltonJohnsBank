# Generated by Django 4.0.4 on 2022-06-05 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Websitebank', '0012_alter_profilepic_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='photos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='nodeflux_photos/')),
            ],
        ),
    ]
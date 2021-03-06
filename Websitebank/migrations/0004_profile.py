# Generated by Django 4.0.4 on 2022-06-01 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Websitebank', '0003_alter_account_user_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.AutoField(db_column='account_id', primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('pin', models.CharField(max_length=6)),
                ('card_no', models.CharField(max_length=16, unique=True)),
                ('balance', models.DecimalField(decimal_places=3, max_digits=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-30 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account_user',
            fields=[
                ('id', models.AutoField(db_column='account_no', primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('pin', models.IntegerField()),
                ('card_no', models.CharField(max_length=16)),
                ('balance', models.DecimalField(decimal_places=3, max_digits=15)),
            ],
        ),
    ]

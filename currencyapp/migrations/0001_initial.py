# Generated by Django 2.2.7 on 2020-08-24 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Link', models.CharField(max_length=200)),
                ('BiggerThan', models.FloatField(default=0)),
                ('SmallerThan', models.FloatField(default=0)),
            ],
        ),
    ]

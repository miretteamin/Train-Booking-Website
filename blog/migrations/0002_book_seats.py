# Generated by Django 3.2.2 on 2021-07-15 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='seats',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 3.2.2 on 2021-07-08 19:53

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210708_2145'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='trip',
            name='SourceDestConstraints',
        ),
        migrations.AlterField(
            model_name='station',
            name='id',
            field=models.IntegerField(default=-1, primary_key=True, serialize=False),
        ),
        migrations.AddConstraint(
            model_name='trip',
            constraint=models.CheckConstraint(check=models.Q(('sourcelte', blog.models.Train.getDest)), name='sourceValid'),
        ),
        migrations.AddConstraint(
            model_name='trip',
            constraint=models.CheckConstraint(check=models.Q(('destinationlte', blog.models.Train.getDest)), name='destValid'),
        ),
    ]
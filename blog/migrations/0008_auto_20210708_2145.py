# Generated by Django 3.2.2 on 2021-07-08 19:45

from django.db import migrations, models
import django.db.models.expressions
import django_db_constraints.operations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210708_2115'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='trip',
            constraint=models.CheckConstraint(check=models.Q(('source__exact', django.db.models.expressions.F('destination')), _negated=True), name='SourceDestConstraints'),
        ),
        django_db_constraints.operations.AlterConstraints(
            name='trip',
            db_constraints={},
        ),
    ]

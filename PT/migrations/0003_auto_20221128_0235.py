# Generated by Django 3.2.16 on 2022-11-27 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PT', '0002_interestplant_please_write_down_the_name_of_the_constraint'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='interestplant',
            name='please_write_down_the_name_of_the_constraint',
        ),
        migrations.AddConstraint(
            model_name='interestplant',
            constraint=models.UniqueConstraint(fields=('userID', 'plantID'), name='Do not allow duplication'),
        ),
    ]

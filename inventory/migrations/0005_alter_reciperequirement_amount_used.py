# Generated by Django 5.1.1 on 2024-09-05 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_ingredient_unit_of_measure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reciperequirement',
            name='amount_used',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

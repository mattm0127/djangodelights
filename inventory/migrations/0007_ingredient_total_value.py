# Generated by Django 5.1.1 on 2024-09-08 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_alter_ingredient_total_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='total_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]

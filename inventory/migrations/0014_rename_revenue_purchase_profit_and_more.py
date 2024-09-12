# Generated by Django 5.1.1 on 2024-09-09 22:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_alter_purchase_menu_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='revenue',
            new_name='profit',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='menu_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.menuitem'),
        ),
        migrations.AlterField(
            model_name='reciperequirement',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.ingredient'),
        ),
    ]

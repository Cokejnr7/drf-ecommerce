# Generated by Django 4.1.7 on 2023-09-17 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='qty',
            field=models.PositiveIntegerField(),
        ),
    ]
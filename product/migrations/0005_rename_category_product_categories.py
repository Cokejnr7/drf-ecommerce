# Generated by Django 4.1.7 on 2023-07-13 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_category_created_category_updated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='categories',
        ),
    ]

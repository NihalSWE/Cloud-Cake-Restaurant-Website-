# Generated by Django 4.2.7 on 2024-06-06 11:13

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_order_created_at_order_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='detail',
            field=ckeditor.fields.RichTextField(max_length=1000, null=True),
        ),
    ]
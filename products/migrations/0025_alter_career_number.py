# Generated by Django 4.2.7 on 2024-07-31 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_designation_career_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='career',
            name='number',
            field=models.IntegerField(),
        ),
    ]

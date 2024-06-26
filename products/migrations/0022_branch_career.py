# Generated by Django 4.2.7 on 2024-06-13 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_remove_outlet_map_url_outlet_map_iframe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.IntegerField(max_length=15)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('message', models.TextField(null=True)),
                ('cv', models.FileField(upload_to='cvs/')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.branch')),
            ],
        ),
    ]

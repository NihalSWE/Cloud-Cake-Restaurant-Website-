# Generated by Django 4.2.7 on 2024-10-30 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0041_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story', models.TextField(max_length=500)),
                ('story_image', models.ImageField(blank=True, null=True, upload_to='about/')),
                ('mission', models.TextField(max_length=500)),
                ('mission_image', models.ImageField(blank=True, null=True, upload_to='about/')),
            ],
        ),
        migrations.CreateModel(
            name='AboutUs_TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='team/')),
            ],
        ),
    ]

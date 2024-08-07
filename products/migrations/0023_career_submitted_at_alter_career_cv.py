# Generated by Django 4.2.7 on 2024-06-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_branch_career'),
    ]

    operations = [
        migrations.AddField(
            model_name='career',
            name='submitted_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='career',
            name='cv',
            field=models.FileField(upload_to='cv_uploads/%Y/%m/%d/'),
        ),
    ]
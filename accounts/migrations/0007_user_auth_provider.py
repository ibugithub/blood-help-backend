# Generated by Django 5.0 on 2024-03-03 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_userotp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth_provider',
            field=models.CharField(default='email', max_length=50),
        ),
    ]

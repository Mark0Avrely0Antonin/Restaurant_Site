# Generated by Django 4.0.4 on 2022-05-23 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_project', '0010_user_account_is_email_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_account',
            name='profile_username',
            field=models.SlugField(blank=True, verbose_name='Профильное имя'),
        ),
    ]

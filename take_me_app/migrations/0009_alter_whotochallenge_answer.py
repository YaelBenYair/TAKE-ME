# Generated by Django 4.1.7 on 2023-06-04 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('take_me_app', '0008_whotochallenge_is_read_whotochallenge_who_challenge_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whotochallenge',
            name='answer',
            field=models.BooleanField(blank=True, db_column='answer', null=True),
        ),
    ]
# Generated by Django 2.2.5 on 2019-09-21 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicalapp', '0002_gamebadge_userpoints'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='badge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='medicalapp.GameBadge'),
        ),
        migrations.AddField(
            model_name='profile',
            name='points',
            field=models.IntegerField(null=True),
        ),
    ]

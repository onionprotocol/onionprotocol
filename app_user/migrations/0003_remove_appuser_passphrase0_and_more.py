# Generated by Django 4.1.3 on 2022-12-03 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0002_appuser_passphrase0_appuser_passphrase1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase0',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase1',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase10',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase11',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase2',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase3',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase4',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase5',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase6',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase7',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase8',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='passphrase9',
        ),
    ]
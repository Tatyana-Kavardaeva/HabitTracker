# Generated by Django 4.2.2 on 2024-10-31 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0008_habit_last_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='last_sent',
        ),
    ]

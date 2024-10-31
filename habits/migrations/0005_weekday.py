# Generated by Django 4.2.2 on 2024-10-31 14:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_alter_habit_periodicity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weekday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=20, verbose_name='День недели')),
                ('number', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)], verbose_name='Порядковый номер дня в неделе')),
            ],
            options={
                'verbose_name': ('День недели',),
                'verbose_name_plural': 'Дни недели',
            },
        ),
    ]
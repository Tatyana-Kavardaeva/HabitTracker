# Generated by Django 4.2.2 on 2024-10-31 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_tg_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tg_chat_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Телеграм chat-id'),
        ),
    ]

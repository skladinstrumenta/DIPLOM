# Generated by Django 4.1.4 on 2023-01-03 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Latrello', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['-pk'], 'verbose_name': 'Карточка', 'verbose_name_plural': 'Карточки'},
        ),
        migrations.AlterField(
            model_name='card',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='executor', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
        ),
    ]

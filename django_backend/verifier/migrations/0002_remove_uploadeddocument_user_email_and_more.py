# Generated by Django 5.2.2 on 2025-06-10 05:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifier', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadeddocument',
            name='user_email',
        ),
        migrations.AddField(
            model_name='uploadeddocument',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='uploadeddocument',
            name='fraud_score',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uploadeddocument',
            name='verdict',
            field=models.CharField(max_length=20),
        ),
    ]

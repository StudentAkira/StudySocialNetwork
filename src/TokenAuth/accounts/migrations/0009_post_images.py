# Generated by Django 3.2.7 on 2022-07-31 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_postimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='images',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.postimage'),
        ),
    ]

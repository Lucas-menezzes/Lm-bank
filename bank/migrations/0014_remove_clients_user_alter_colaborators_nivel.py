# Generated by Django 5.0.2 on 2024-02-28 18:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bank", "0013_alter_colaborators_nivel"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="clients",
            name="user",
        ),
        migrations.AlterField(
            model_name="colaborators",
            name="nivel",
            field=models.CharField(
                choices=[("G", "Gerente"), ("B", "Bancario")], default="B", max_length=1
            ),
        ),
    ]

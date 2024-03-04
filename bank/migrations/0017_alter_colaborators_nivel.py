# Generated by Django 5.0.2 on 2024-02-28 19:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bank", "0016_alter_colaborators_nivel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="colaborators",
            name="nivel",
            field=models.CharField(
                choices=[("B", "Bancario"), ("G", "Gerente")], default="B", max_length=1
            ),
        ),
    ]

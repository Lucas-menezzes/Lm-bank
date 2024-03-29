# Generated by Django 5.0.2 on 2024-03-05 15:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bank", "0021_alter_colaborators_nivel"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="profile",
            field=models.CharField(default="undefined", max_length=255),
        ),
        migrations.AlterField(
            model_name="colaborators",
            name="nivel",
            field=models.CharField(
                choices=[("B", "Bancario"), ("G", "Gerente")], default="B", max_length=1
            ),
        ),
    ]

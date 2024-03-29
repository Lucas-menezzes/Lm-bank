# Generated by Django 5.0.2 on 2024-03-05 15:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bank", "0022_customuser_profile_alter_colaborators_nivel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="colaborators",
            name="nivel",
            field=models.CharField(
                choices=[("G", "Gerente"), ("B", "Bancario")], default="B", max_length=1
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="profile",
            field=models.CharField(
                choices=[
                    ("admin", "Administrador"),
                    ("manager", "Gerente"),
                    ("colaborator", "Colaborador"),
                    ("client", "Cliente"),
                ],
                default="undefined",
                max_length=255,
            ),
        ),
    ]

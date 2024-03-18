# Generated by Django 4.2 on 2024-02-13 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service", "0002_payment"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClearAmount",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.TextField()),
                ("count", models.IntegerField(default=0)),
                ("tarif", models.CharField(default="Пробный", max_length=100)),
            ],
        ),
    ]
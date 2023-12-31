# Generated by Django 5.0 on 2023-12-28 23:31

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Category", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("title", models.CharField(max_length=60)),
                ("description", models.TextField(max_length=800)),
                (
                    "price",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                0, "Price cannot be negative"
                            )
                        ]
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Category.category",
                    ),
                ),
            ],
        ),
    ]

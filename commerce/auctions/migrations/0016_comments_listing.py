# Generated by Django 5.0.1 on 2024-02-08 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0015_comments"),
    ]

    operations = [
        migrations.AddField(
            model_name="comments",
            name="listing",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="auctions.listing",
            ),
        ),
    ]

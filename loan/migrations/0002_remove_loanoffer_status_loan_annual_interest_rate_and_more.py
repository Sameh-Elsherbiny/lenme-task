# Generated by Django 5.1.4 on 2024-12-08 17:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanoffer',
            name='status',
        ),
        migrations.AddField(
            model_name='loan',
            name='annual_interest_rate',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loan',
            name='lender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funded_loans', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='loan',
            name='lenme_fee',
            field=models.DecimalField(decimal_places=2, default=3.75, max_digits=10),
        ),
        migrations.DeleteModel(
            name='MonthlyPayment',
        ),
    ]

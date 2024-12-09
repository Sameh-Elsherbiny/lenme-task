# Generated by Django 5.1.4 on 2024-12-08 22:00

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0003_alter_loan_annual_interest_rate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loan',
            options={'verbose_name': 'Loan', 'verbose_name_plural': 'Loans'},
        ),
        migrations.AlterModelOptions(
            name='loanoffer',
            options={'verbose_name': 'Loan Offer', 'verbose_name_plural': 'Loan Offers'},
        ),
        migrations.AddField(
            model_name='loan',
            name='counter',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='loan',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='LoanRepayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('repayment_date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repayments', to='loan.loan')),
            ],
            options={
                'verbose_name': 'Loan Repayment',
                'verbose_name_plural': 'Loan Repayments',
            },
        ),
    ]
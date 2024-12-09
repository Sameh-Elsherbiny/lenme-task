from django.db import models
from core.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Loan(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Funded', 'Funded'),
        ('Completed', 'Completed')
    )
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.PositiveIntegerField(help_text="Loan period in months")
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Funded', 'Funded'), ('Completed', 'Completed')], default='Pending')
    funded_date = models.DateField(null=True, blank=True)
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='funded_loans', null=True, blank=True)
    annual_interest_rate = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null=True)
    lenme_fee = models.DecimalField(max_digits=10, decimal_places=2, default=3.75)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)
    counter = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return f'{self.borrower} requests a loan of ${self.amount}'
    
    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'


class LoanOffer(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='offers')
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_offers')
    annual_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    lenme_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.lender} offers {self.loan} at {self.annual_interest_rate}%'
    
    class Meta:
        verbose_name = 'Loan Offer'
        verbose_name_plural = 'Loan Offers'


class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    repayment_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f'{self.loan} repayment of ${self.amount} on {self.repayment_date}'
    
    class Meta:
        verbose_name = 'Loan Repayment'
        verbose_name_plural = 'Loan Repayments'

 

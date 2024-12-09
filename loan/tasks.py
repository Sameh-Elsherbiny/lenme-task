from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Loan, LoanRepayment
from core.models import Account
from django.db import transaction


@shared_task
def schedule_repayments():
    print("Scheduling repayments")
    if timezone.now().date().day == 1:
        loans = Loan.objects.filter(status="Funded")
        for loan in loans:
            period = loan.period
            amount = loan.amount
            lenme_fee = loan.lenme_fee / 100
            annual_interest_rate = loan.annual_interest_rate / 100 + lenme_fee
            monthly_interest_rate = annual_interest_rate / 12
            monthly_payment = (
                amount
                * (monthly_interest_rate * (1 + monthly_interest_rate) ** period)
                / ((1 + monthly_interest_rate) ** period - 1)
            )
            payment =  LoanRepayment.objects.create(
                loan=loan, amount=monthly_payment, repayment_date=timezone.now()
            )
            lender_account = Account.objects.get(user=loan.lender)
            borrower_account = Account.objects.get(user=loan.borrower).balance
            if borrower_account < monthly_payment:
                continue ;
            borrower_account -= monthly_payment
            lender_account.balance += monthly_payment
            lender_account.save()
            borrower_account.save()
            payment.status = "Completed"
            payment.save()
            loan.counter += 1

@shared_task
def complete_loan():
    loans = Loan.objects.filter(status="Funded")
    for loan in loans:
        if loan.counter == loan.period:
            loan.status = "Completed"
            loan.save()
    return loan

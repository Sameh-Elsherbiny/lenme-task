from rest_framework import serializers
from .models import Loan, LoanOffer ,LoanRepayment
from core.models import  Account 
from django.utils import timezone


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = ['id', 'borrower', 'amount', 'period', 'status', 'funded_date', 'lender', 'annual_interest_rate', 'lenme_fee']
        read_only_fields = ['status', 'funded_date','lenme_fee','borrower']


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class LoanOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanOffer
        fields = ['id', 'loan', 'lender', 'annual_interest_rate', 'lenme_fee']
        read_only_fields = ['lenme_fee']

    def validate(self, attrs):
        loan = attrs.get('loan')
        lender = self.context['request'].user
        account =  Account.objects.get(user=lender)
        if account.balance < loan.amount:
            raise serializers.ValidationError("Insufficient balance to fund this loan.")

        # Ensure loan is still pending
        if loan.status != 'Pending':
            raise serializers.ValidationError("This loan is no longer available for offers.")
        return attrs

class AcceptOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOffer
        fields = '__all__'



    def update(self, instance, validated_data):
        loan = instance.loan
        
        lender = instance.lender
        lender_account = Account.objects.get(user=lender)
        print(lender_account.balance,loan.amount)
        if lender_account.balance < loan.amount:
            raise serializers.ValidationError("Insufficient balance to fund this loan.")
        borrower = instance.loan.borrower
        borrower_account = Account.objects.get(user=borrower)
        lender_account.balance -= loan.amount
        borrower_account.balance += loan.amount
        instance.loan.status = 'Funded'
        loan.status = 'Funded'
        loan.funded_date = timezone.now()
        loan.annual_interest_rate = instance.annual_interest_rate
        loan.save()
        lender_account.save()
        borrower_account.save()
        return instance
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = '__all__'
    
    def create(self, validated_data):
        loan_id = validated_data.get('loan')
        loan = Loan.objects.get(id=loan_id)
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
            raise serializers.ValidationError("Insufficient balance to make this payment.")
        borrower_account -= monthly_payment
        lender_account.balance += monthly_payment
        lender_account.save()
        borrower_account.save()
        payment.status = "Completed"
        payment.save()
        loan.counter += 1
        return payment

    def update(self, instance, validated_data):
        if instance.status == 'Completed':
            raise serializers.ValidationError("This repayment has already been completed.")
        return super().update(instance, validated_data)






from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Loan , LoanOffer 
from core.models import Account

User = get_user_model()

class LoanRequestViewTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(email='testuser@email.com', password='testpassword',is_active=True)
        self.client.login(email='testuser@email.com', password='testpassword')

        # Define test data
        self.loan_data = {
            "amount": 5000,
            "period": 6,
            "annual_interest_rate": 15.0,  # 15% APR
        }
    def test_create_loan_request(self):
            # Log in the user and get the token
            response = self.client.post('/api/token/', {'email': 'testuser@email.com', 'password': 'testpassword'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            token = response.data['access']
    
            # Set the token in the authorization header
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
            # Send a POST request to create a loan
            self.response = self.client.post('/loan/loanrequestview/', self.loan_data)
    
            # Check if the request was successful
            self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
    
            # Verify the loan was created with correct data
            loan = Loan.objects.get(id=self.response.data['id'])
            self.assertEqual(loan.borrower, self.user)
            self.assertEqual(loan.amount, self.loan_data['amount'])
            self.assertEqual(loan.period, self.loan_data['period'])
            self.assertEqual(loan.annual_interest_rate, self.loan_data['annual_interest_rate'])
            
    def test_create_loan_request_unauthenticated(self):
        # Log out the user
        self.client.logout()

        # Send a POST request to create a loan
        response = self.client.post('/loan/loanrequestview/', self.loan_data)

        # Ensure the request is unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



User = get_user_model()

class SubmitOfferViewTestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.borrower = User.objects.create_user(email='borrower@email.com', password='testpassword',is_active=True)
        self.lender = User.objects.create_user(email='lender@email.com', password='testpassword',is_active=True)
        self.client.login(email='lender@email.com', password='testpassword')

        # Create accounts with balances
        self.borrower_account = Account.objects.create(user=self.borrower, balance=0)
        self.lender_account = Account.objects.create(user=self.lender, balance=10000)

        

        # Create a loan
        self.loan = Loan.objects.create(
            borrower=self.borrower,
            amount=5000,
            period=6,
            status='Pending',
            annual_interest_rate=15.0
        )

        # Set up test loan offer data
        self.offer_data = {
            'loan': self.loan.id,
            'annual_interest_rate': 15.0,
            'lender' : self.lender.id
        }

    def test_submit_offer_success(self):
        # Log in as the lender
        response = self.client.post('/api/token/', {'email': 'lender@email.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
                                    
        # Submit the loan offer
        response = self.client.post('/loan/submitofferview/', self.offer_data)

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if the loan offer was created
        loan_offer = LoanOffer.objects.get(id=response.data['id'])
        self.assertEqual(loan_offer.loan, self.loan)
        self.assertEqual(loan_offer.lender, self.lender)
        self.assertEqual(loan_offer.annual_interest_rate, self.offer_data['annual_interest_rate'])

    def test_submit_offer_insufficient_balance(self):
        # Reduce lender's balance to below loan amount
        self.lender_account.balance = 1000
        self.lender_account.save()

        # Log in as the lender
        response = self.client.post('/api/token/',{'email': 'lender@email.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Submit the loan offer
        response = self.client.post('/loan/submitofferview/', self.offer_data)

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Insufficient balance', response.data['non_field_errors'][0])

    def test_submit_offer_non_pending_loan(self):
        # Log in as the lender
        response = self.client.post('/api/token/',{'email': 'lender@email.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Change the loan status to 'Funded'
        self.loan.status = 'Funded'
        self.loan.save()

        # Submit the loan offer
        response = self.client.post('/loan/submitofferview/', self.offer_data)

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This loan is no longer available for offers.', response.data['non_field_errors'][0])

    def test_submit_offer_unauthenticated(self):
        # Submit the loan offer without logging in
        response = self.client.post('/loan/submitofferview/', self.offer_data)

        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
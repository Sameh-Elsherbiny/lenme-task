from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Loan, LoanOffer ,LoanRepayment
from .serializers import LoanSerializer, LoanOfferSerializer,AcceptOfferSerializer , PaymentSerializer



class LoanRequestView(CreateAPIView):
    serializer_class = LoanSerializer  
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)


class UnfundedLoansListView(ListAPIView):
    queryset = Loan.objects.filter(status='Pending')
    serializer_class = LoanSerializer  

class SubmitOfferView(CreateAPIView):
    serializer_class = LoanOfferSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(lender=self.request.user)


class AcceptOfferView(UpdateAPIView):
    serializer_class = AcceptOfferSerializer
    permission_classes = [IsAuthenticated]
    queryset = LoanOffer.objects.all()


class ListPaymentView(ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Loan.objects.all()

    def get_queryset(self):
        return LoanRepayment.objects.filter(loan__borrower=self.request.user)


class UpdatePaymentView(UpdateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LoanRepayment.objects.filter(loan__borrower=self.request.user)
    
class CreatePaymentView(CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    





    

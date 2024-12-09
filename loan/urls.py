from django.urls import path
from .views import LoanRequestView , UnfundedLoansListView , SubmitOfferView , AcceptOfferView , ListPaymentView , UpdatePaymentView , CreatePaymentView

urlpatterns = [
    path('loanrequestview/', LoanRequestView.as_view(), name='loanrequestview'),
    path('unfundedloanslistview/', UnfundedLoansListView.as_view(), name='unfundedloanslistview'),
    path('submitofferview/', SubmitOfferView.as_view(), name='submitofferview'),
    path('acceptofferview/<int:pk>/', AcceptOfferView.as_view(), name='acceptofferview'),
    path('listpaymentview/', ListPaymentView.as_view(), name='listpaymentview'),
    path('updatepaymentview/<int:pk>/', UpdatePaymentView.as_view(), name='updatepaymentview'),
    path('createpaymentview/', CreatePaymentView.as_view(), name='createpaymentview'),
]
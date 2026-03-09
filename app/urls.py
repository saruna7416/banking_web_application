from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="home"),
    path('create',views.create,name="create"),
    path('cash_withdraw',views.cash_withdraw,name="cash_withdraw"),
    path('deposite',views.deposite,name="deposite"),
    path('pincode',views.pincode,name="pincode"),
    path('transfer',views.transfer,name="transfer"),
    path('user',views.user,name="user"),
    path('wallet',views.wallet,name="wallet"),
    path('otp',views.otp_validation , name="otp")
]
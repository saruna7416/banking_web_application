from django.shortcuts import render , HttpResponse , redirect
from .models import Account
from django.core.mail import send_mail
from django.conf import settings
from random import randint
import  hashlib 
import time 
from decimal import Decimal as de
# Create your views here.
def index(request):
    return render(request,'index.html')

def create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        mail = request.POST.get("mail")
        add = request.POST.get("add")
        gen = request.POST.get("gen")
        date = request.POST.get("date")
        aaddhar = request.POST.get("aadhar")
        # print(name,phone,mail,add,gen,date,aaddhar)
        Account.objects.create(name = name,phone = phone , email = mail, address = add , aadhar = aaddhar , dob = date , gender = gen)
        var = Account.objects.get(phone = phone)
        send_mail("Account created successfully",f"this is ur account number {var.account_num} , enjoy our servies \n thank you \n regards \n manager of FINOVA bank",settings.EMAIL_HOST_USER,[var.email],fail_silently=False)
        # print(var.account_num)
        return HttpResponse("account created")
    return render(request,'create.html')

def cash_withdraw(request):
    msg = ""
    
    if request.method == "POST":
        acc = int(request.POST.get('acc'))
        pin = request.POST.get('pin')
        amt = de(request.POST.get('amt'))  
        
        data = Account.objects.get(account_num=acc)
        npin = encrypt(str(pin))
        
        if data.pin == npin:
            if amt > de("100"):
                if amt <= de("10000"):
                    data.balance -= amt
                    data.save()
                    send_mail(
                        "WITHDRAW",
                        f"mi bank account lo nunchi aksharala {amt} rs sai ram\nthank you boss\nlove you bache",
                        settings.EMAIL_HOST_USER,
                        [data.email],
                        fail_silently=False
                    )
                    return redirect("home")
                else:
                    msg = "amt is aukat ke bahar"
            else:
                msg = "amt should be greater than 500"
        

    return render(request,'cashwithdraw.html')

def deposite(request):
    msg = ""
    if request.method == "POST":
        acc = request.POST.get('acc')
        pin = request.POST.get('pin')
        amt = int(request.POST.get('amt'))
        try:
            data = Account.objects.get(account_num = acc)
        except Exception as e:
            msg = e
        if data:
            npin = encrypt(str(pin))
            if data.pin == npin:
                if amt>100:
                    if amt<=10000:
                        data.balance += amt
                        data.save()
                        send_mail("DEPOSIT",f"mi bank account loki aksharala  {amt} rs vachi padayi \n thank you boss \n love you bache " ,settings.EMAIL_HOST_USER,[data.email],fail_silently=False)
                        return redirect("home")
                    else:
                        msg = "amt is aukat ke bahar"
                else:
                    msg = "amt should be greater than 500"
    return render(request,'deposite.html',{"msg":msg})

def pincode(request):
    if request.method == "POST":
        acc = request.POST.get("acc")
        data = Account.objects.get(account_num = acc)
        otp = randint(100000,999999)
        # print(otp)
        request.session['otp'] = otp
        send_mail("PIN GENERATION ",f"ur one time password is {otp} please share it with our scamers only" ,settings.EMAIL_HOST_USER,[data.email],fail_silently=False)
        return redirect('otp')
    return render(request,'pincode.html')

def transfer(request):
    msg = ""
    if request.method == "POST":
        sender_acc = request.POST.get("sender_acc")
        receiver_acc = request.POST.get("receiver_acc")
        pin = request.POST.get("pin")
        amt = de(request.POST.get("amt"))

        try:
            sender = Account.objects.get(account_num=sender_acc)
            receiver = Account.objects.get(account_num=receiver_acc)
        except Account.DoesNotExist:
            msg = "Invalid account number(s)"
            return render(request, "transfer.html", {"msg": msg})

       
        npin = encrypt(str(pin))     # verify sender's pin
        if sender.pin != npin:
            msg = "Incorrect PIN"
            return render(request, "transfer.html", {"msg": msg})

       
        if sender.balance < amt:     # check balance
            msg = "Insufficient balance"
            return render(request, "transfer.html", {"msg": msg})

        if amt < de("100"):
            msg = "Transfer amount must be at least 100"
            return render(request, "transfer.html", {"msg": msg})

        if amt > de("50000"):
            msg = "Transfer limit exceeded (max 50,000)"
            return render(request, "transfer.html", {"msg": msg})

       
        sender.balance -= amt    # debit sender, credit receiver
        receiver.balance += amt
        sender.save()
        receiver.save()

        # email notifications
        send_mail(                                  
            "Cash Transfer Successful",
            f"You have transferred {amt} Rs to account {receiver.account_num}. "
            f"Your remaining balance is {sender.balance}.",
            settings.EMAIL_HOST_USER,
            [sender.email],
            fail_silently=False
        )

        send_mail(
            "Cash Received",
            f"You have received {amt} Rs from account {sender.account_num}. "
            f"Your updated balance is {receiver.balance}.",
            settings.EMAIL_HOST_USER,
            [receiver.email],
            fail_silently=False
        )

        return redirect("home")

    return render(request, "transfer.html", {"msg": msg})
    

def user(request):
    if request.method == "POST":
        a = Account.objects.get(account_num = request.POST.get('acc'))
        a.delete()
        return redirect("home")
    return render(request,'user.html')

def encrypt(data):
    return hashlib.shake_256(data.encode()).hexdigest(length=32)
def wallet(request):
    msg = ""
    if request.method == "POST":
        acc = request.POST.get('acc')
        pin = request.POST.get('pin')
        try:
            data = Account.objects.get(account_num = acc)
        except Exception as e:
            msg = e
        if data:
            npin = encrypt(str(pin))
            if data.pin == npin:
                msg = data.balance
                return redirect("home")
            else:
                msg = "pin is in correct"

        time.sleep(5)
    return render(request,'wallet.html',{'msg':msg})
    




def otp_validation(request):
    msg = ""
    late_otp = request.session['otp']
    if request.method == "POST":
        phone = int(request.POST.get('mobile'))
        notp = int(request.POST.get('notp'))
        cotp = int(request.POST.get('cotp'))
        npin = int(request.POST.get('npin'))
        cpin = int(request.POST.get('cpin'))
        # print(phone,notp,npin,cotp,cpin)
        if notp == cotp:
            if npin == cpin:
                data = Account.objects.get(phone = phone)
                # data.pin = npin
                data.pin = encrypt(str(npin))
                data.save()
                msg = "pin genrated successfully"
                send_mail("PIN GENERATED SUCCESSFULLY ","the pin has been generated and set to ur account please don't x=share it with other scamers only share with us \n thank you \n love you bache \n regards \n ibmc manager",settings.EMAIL_HOST_USER,[data.email],fail_silently=False)
            else:
                msg = "pin mismatch"
        else:
            msg = "otp mismatch"
    return render(request,"otp_validation.html",{"msg":msg})


from django.db.models.fields import PositiveBigIntegerField
from django.http.response import ResponseHeaders
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

from .models import *


def login(request):
    data = ""
    return render(request, 'login.html', {"data": data})

def verifyLogin(request):
    post_data = request.POST
    print(post_data)
    if 'username' and 'pass':
        user = authenticate(
            request,
            username = post_data['username'],
            password = post_data['pass']
        )
        if user is None:
            return redirect('login')
        elif user.is_superuser:
            auth_login(request, user)
            return redirect('/')
        else:
            auth_login(request, user)
            return redirect('salesdashboard')

    else:
        return redirect('login')

def userLogout(request):
    logout(request)
    return redirect('login')

def register(request):
    data = ""
    return render(request, 'register.html', {"data": data})

def addUser(request):
    data = ""
    return render(request, "user_add.html", {"data": data})

def registerUser(request):
    post_data = request.POST
    username = post_data['email']
    if User.objects.filter(username=username).exists():
        alert = "User Already Exists"
        return render(request, "user_add.html", {"alert": alert})
    elif post_data['pass'] != post_data['conf_pass']:
        alert = "password didn't match"
        return render(request, "user_add.html", {"alert": alert})
    else:
        user = User.objects.create_user(post_data['email'], post_data['email'], post_data['pass'])
        dashboardUser = DashboardUser(
            user = user,
            username = post_data['email'],
            email = post_data['email']
        )
        subject = 'Welcome to Absolute Point'
        message = f'Hi {dashboardUser.username}, Your Account has been Created please login to the system with your email and password.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [dashboardUser.email, ]
        send_mail( subject, message, email_from, recipient_list )
        dashboardUser.save()
        return redirect('/')

def resetPassword(request):
    data = ""
    return render(request, "passwordreset.html", {"data": data})

def changePassword(request):
    user = request.user
    post_data = request.POST

    if post_data['pass'] != post_data['conf_pass']:
        alert = "Please enter the same password for both input"
        return render(request, 'passwordreset.html', {"alert": alert})
    else:
        user.set_password(post_data['pass'])
        user.save()
        logout(request)
        return redirect('login')


def updateUser(request):
    post_data = request.POST
    dashuser = DashboardUser.objects.get(user_id = post_data['id'])
    dashuser.name = post_data['name']
    dashuser.phone = post_data['phone']
    dashuser.address = post_data['address']
    dashuser.status = True
    dashuser.save()
    return redirect('salesdashboard')


@login_required(login_url="/login/")
def salesDashboard(request):
    data = ""
    notices = Notices.objects.all()
    services = Services.objects.all()
    servicelist = Service.objects.all()
    info = DashboardUser.objects.get(user_id=request.user.id)
    return render(request, 'sales_dashboard.html', 
        {"data": data, "notices": notices, "services": services, "info": info, "servicelist": servicelist})


@login_required(login_url='/login/')
def home(request):
    data = ""
    notices = Notices.objects.all()
    services = Services.objects.all()
    servicelist = Service.objects.all()
    servicetypes = ServiceType.objects.all()
    users = User.objects.all()
    return render(request, 'index.html', 
        {"data": data, "notices": notices, "services": services, "users": users, 
            "servicelist": servicelist, "servicetypes": servicetypes})
    # return render(request, 'index.html', {"data": data})

def noticeCreate(request):
    data = ""
    return render(request, 'notice_create.html', {"data": data})

def saveNotice(request):
    post_data = request.POST
    notice = Notices(
        title=post_data['title'],
        category=post_data['category'],
        description=post_data['description'],
        validity=post_data['validity']
    )

    notice.save()
    return redirect('/')

def noticeDetail(request, nid):
    data = ""
    notice = Notices.objects.get(id=nid)
    return render(request, 'notice_detail.html', {"data": data, "notice": notice})

def serviceCreate(request):
    data = ""
    servicelist = Service.objects.all()
    servicetypes = ServiceType.objects.all()
    return render(request, 'service_create.html', {"data": data, "servicelist": servicelist, "servicetypes": servicetypes})

def saveService(request):
    post_data = request.POST
    user = request.user
    dashboarduser = DashboardUser.objects.filter(user_id=user.id).last()
    service_title = Service.objects.get(id=post_data['service'])
    service_type = ServiceType.objects.get(id=post_data['service_type'])
    service = Services(
        user=dashboarduser,
        title=post_data['title'],
        service_type=service_type,
        service=service_title,
        site_name=post_data['site_name'],
        site_url=post_data['site_url'],
        counter=post_data['counter'],
        ratio=post_data['ratio'],
        price=post_data['price']
    )
    service.save()
    service.status = "Accept Pending"
    service.payment_status = "Due"
    service.save()

    return redirect('salesdashboard')

def addService(request):
    data = ""
    return render(request, 'service_add.html', {"data": data})

def addServiceList(request):
    post_data = request.POST

    service = Service(
        title = post_data['title'],
        quantity = post_data['quantity'],
        price = post_data['price'],
    )
    service.save()
    return redirect('/')

def updateServiceList(request):
    post_data = request.POST
    service = Service.objects.get(id=post_data['service'])
    service.quantity = post_data['quantity']
    service.price = post_data['price']
    service.save()
    return redirect('/')

def addServiceType(request):
    data = ""
    return render(request, 'service_add_type.html', {"data": data})

def addServiceTypeList(request):
    post_data = request.POST

    servicetype = ServiceType(
        title = post_data['title'],
    )
    servicetype.save()
    return redirect('/')
    

def serviceDetail(request, sid):
    data = ""    
    toPay = True
    paid = 0.0    
    service = Services.objects.get(id=sid)
    payments = ServicePayments.objects.filter(service__id=sid)
    remaining = service.price
    for payment in payments:
        if payment.accepted:
            paid += payment.amount
            remaining -= payment.amount


    if paid >= service.price:
        toPay = False

    return render(request, 'service_detail.html', {"data": data, "service": service, "payments": payments, "paid": paid, "remaining": remaining, "toPay": toPay})

def acceptService(requset, sid):
    service = Services.objects.get(id=sid)
    service.accepted = True
    service.status = "Started"
    service.save()

    return redirect('servicedetail', sid)

def addServicePyament(request):
    post_data = request.POST
    if request.FILES['image']:
        image = request.FILES['image']
    else:
        image = None

    service = Services.objects.get(id=post_data['id'])
    payment = ServicePayments(
        service = service,
        amount = post_data['amount'],
        link = post_data['link'],
        image = image,
    )
    payment.save()
    return redirect('servicedetail', service.id)

def acceptPayment(request, pid):
    payment = ServicePayments.objects.get(id=pid)
    payment.accepted = True
    payment.save()

    return redirect('servicedetail', payment.service.id)

def donePayment(request, sid):
    service = Services.objects.get(id=sid)
    service.payment_status = "Received"
    service.status = "Completed"
    service.save()

    return redirect('servicedetail', sid)


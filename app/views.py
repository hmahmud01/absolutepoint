from django.db.models.fields import PositiveBigIntegerField
from django.http.response import ResponseHeaders
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
import json

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
        else:
            auth_login(request, user)
            return redirect('/')
        # else:
        #     req_user = DashboardUser.objects.get(user=user.id)
        #     if req_user.user_type == 'sales':
        #         auth_login(request, user)
        #         return redirect('salesdashboard')

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
    add_user = True
    return render(request, "user_add.html", {"data": data, "add_user": add_user})

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

        user_rank = UserRank(
            user=dashboardUser,
            title="NOOB",
            tier=0,
            sale_percent=5.0,
            current_earn=0.0
        )

        user_rank.save()

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
    dashuser.email = post_data['email']
    dashuser.username=post_data['email']
    dashuser.phone = post_data['phone']
    dashuser.address = post_data['address']
    dashuser.status = True
    dashuser.save()
    user = dashuser.user
    user.username = post_data['email']
    user.email = post_data['email']
    user.save()

    try:
        user_rank = UserRank.objects.get(user_id=dashuser.id)
        print(user_rank)
    except:
        pass
    return redirect('/')

def reupdateUser(request):
    post_data = request.POST
    dashuser = DashboardUser.objects.get(id = post_data['id'])
    dashuser.name = post_data['name']
    dashuser.email = post_data['email']
    dashuser.username=post_data['email']
    dashuser.phone = post_data['phone']
    dashuser.address = post_data['address']
    dashuser.status = True
    dashuser.save()
    user = dashuser.user
    user.username = post_data['email']
    user.email = post_data['email']
    user.save()

    try:
        user_rank = UserRank.objects.get(user_id=dashuser.id)
        print(user_rank)
    except:
        pass
    return redirect('/')

def detailUser(request, uid):
    info = DashboardUser.objects.get(user_id=uid)
    try:
        rank = UserRank.objects.get(user_id=info.id)
        return render(request, 'user_detail.html', {"info": info, "rank": rank})
    except:
        return render(request, 'user_detail.html', {"info": info})

    
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
    user = request.user
    home = True
    if user.is_superuser:
        data = ""        
        notices = Notices.objects.all()
        services = Services.objects.all().order_by('-created_at')
        servicelist = Service.objects.all()
        servicetypes = ServiceType.objects.all()
        users = User.objects.all().exclude(is_superuser=True)
        return render(request, 'index.html', 
            {"data": data, "notices": notices, "services": services, "users": users, 
                "servicelist": servicelist, "servicetypes": servicetypes, "home": home})
    else:
        req_user = DashboardUser.objects.get(user=user.id)
        if req_user.user_type == 'sales':
            try:
                data = ""
                notices = Notices.objects.all()
                services = Services.objects.all().order_by('-created_at')
                servicelist = Service.objects.all()            
                info = DashboardUser.objects.get(user_id=request.user.id)
                rank = UserRank.objects.get(user_id=info.id)
                print(rank.title)
                return render(request, 'sales_dashboard.html', 
                    {"data": data, "notices": notices, "services": services, "info": info, "servicelist": servicelist, "rank": rank, "home": home})
            except:
                data = ""
                notices = Notices.objects.all()
                services = Services.objects.all().order_by('-created_at')
                servicelist = Service.objects.all()            
                info = DashboardUser.objects.get(user_id=request.user.id)
                return render(request, 'sales_dashboard.html', 
                    {"data": data, "notices": notices, "services": services, "info": info, "servicelist": servicelist, "home": home})
            

    # return render(request, 'index.html', {"data": data})

def noticeCreate(request):
    data = ""
    note_create = True
    return render(request, 'notice_create.html', {"data": data, "note_create": note_create})

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
    service_create = True
    try:
        info = DashboardUser.objects.get(user_id=request.user.id)
        rank = UserRank.objects.get(user_id=info.id)
        return render(request, 'service_create.html', {"data": data, "servicelist": servicelist, "servicetypes": servicetypes, "info": info, "rank": rank, "service_create": service_create})
    except:
        return render(request, 'service_create.html', {"data": data, "servicelist": servicelist, "servicetypes": servicetypes, "service_create": service_create})

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
        price=int(float(post_data['price']))
    )
    service.save()
    service.status = "Pending"
    service.payment_status = "Due"
    service.save()

    return redirect('/')

def addService(request):
    data = ""
    add_service = True
    return render(request, 'service_add.html', {"data": data, "add_service": add_service})

def addServiceList(request):
    post_data = request.POST

    service = Service(
        title = post_data['title'],
        quantity = post_data['quantity'],
        price = post_data['price'],
    )
    service.save()
    return redirect('/')

def removeServiceList(request, sid):
    service = Service.objects.get(id=sid)
    service.delete()

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
    service_type = True
    return render(request, 'service_add_type.html', {"data": data, "service_type": service_type})

def addServiceTypeList(request):
    post_data = request.POST

    servicetype = ServiceType(
        title = post_data['title'],
    )
    servicetype.save()
    return redirect('/')
    
def removeServiceTypeList(request, sid):
    service_type = ServiceType.objects.get(id=sid)
    service_type.delete()

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
        service.payment_status = "Received"
        service.status = "Done"
    
    try:
        info = DashboardUser.objects.get(user_id=request.user.id)
        rank = UserRank.objects.get(user_id=info.id)
        return render(request, 'service_detail.html', {"data": data, "service": service, "payments": payments, "paid": paid, "remaining": remaining, "toPay": toPay, "info": info, "rank": rank})
    except:
        return render(request, 'service_detail.html', {"data": data, "service": service, "payments": payments, "paid": paid, "remaining": remaining, "toPay": toPay})

def acceptService(requset, sid):
    service = Services.objects.get(id=sid)
    service.accepted = True
    service.status = "Working"
    service.save()

    return redirect('servicedetail', sid)

def addServicePyament(request):
    post_data = request.POST
    if request.FILES:
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
    CAP_0 = 0
    CAP_1 = 500
    CAP_2 = 1000
    CAP_3 = 1500
    CAP_4 = 5000

    TIER_0 = 0
    TIER_0_TITLE = "NOOB"
    TIER_0_PERCENT = 5.0
    TIER_1 = 1
    TIER_1_TITLE = "EXPERT"
    TIER_1_PERCENT = 8.0
    TIER_2 = 2
    TIER_2_TITLE = "MASTER"
    TIER_2_PERCENT = 10.0
    TIER_3 = 3
    TIER_3_TITLE = "LEGEND"
    TIER_3_PERCENT = 12.0
    TIER_4 = 4
    TIER_4_TITLE = "BONUS"
    TIER_4_PERCENT = 1.0


    payment = ServicePayments.objects.get(id=pid)
    payment.accepted = True
    payment.save()

    se = payment.service.user
    print(se.id)


    toPay = True
    paid = 0.0    
    payments = ServicePayments.objects.filter(service__id=payment.service.id)
    remaining = payment.service.price
    for payment in payments:
        if payment.accepted:
            paid += payment.amount
            remaining -= payment.amount

    if paid >= payment.service.price:
        toPay = False
        payment.service.payment_status = "Received"
        payment.service.status = "Done"
        payment.service.save()
        payment.save()

    total_sales = 0.0
    tier = 0
    title = ""
    sale_percent = 0.0
    current_earn = 0.0
    sales = ServicePayments.objects.filter(service__user__id=se.id).filter(accepted=True)
    for sale in sales:
        print(sale.amount)
        total_sales += sale.amount
    
    if total_sales > CAP_0 and total_sales < CAP_1:
        tier = TIER_0
        title = TIER_0_TITLE
        sale_percent = TIER_0_PERCENT
        current_earn = total_sales / 100 * sale_percent 
        print(TIER_0_TITLE)
    elif total_sales > CAP_1 and total_sales < CAP_2:
        tier = TIER_1
        title = TIER_1_TITLE
        sale_percent = TIER_1_PERCENT
        current_earn = total_sales / 100 * sale_percent 
        print(TIER_1_TITLE)
    elif total_sales > CAP_2 and total_sales < CAP_3:
        tier = TIER_2
        title = TIER_2_TITLE
        sale_percent = TIER_2_PERCENT
        current_earn = total_sales / 100 * sale_percent 
        print(TIER_2_TITLE)
    elif total_sales > CAP_3 and total_sales < CAP_4:
        tier = TIER_3
        title = TIER_3_TITLE
        sale_percent = TIER_3_PERCENT
        current_earn = total_sales / 100 * sale_percent 
        print(TIER_3_TITLE)
    elif total_sales >= CAP_4:
        tier = TIER_4
        title = TIER_4_TITLE
        sale_percent = TIER_4_PERCENT
        current_earn = total_sales / 100 * sale_percent 
        print(TIER_4_TITLE)

    
    try:
        user_rank = UserRank.objects.get(user_id=se.id)
        user_rank.title=title
        user_rank.tier=tier
        user_rank.sale_percent=sale_percent
        user_rank.current_earn=current_earn

        user_rank.save()
    except:
        user_rank = UserRank(
            user=se,
            title=title,
            tier=tier,
            sale_percent=sale_percent,
            current_earn=current_earn
        )
        user_rank.save()
    
    return redirect('servicedetail', payment.service.id)

def donePayment(request, sid):
    service = Services.objects.get(id=sid)
    service.payment_status = "Received"
    service.status = "Done"
    service.save()

    return redirect('servicedetail', sid)

def fraudPayment(request, sid):
    service = Services.objects.get(id=sid)
    service.payment_status = "Fraud"
    service.status = "Failed"
    service.save()

    return redirect('servicedetail', sid)

def otherPayment(request, sid):
    service = Services.objects.get(id=sid)    
    post_data = request.POST
    if post_data['payment'] == "Received":
        payment = ServicePayments(
            service=service,
            amount=service.price,
            link="Auto Received",
            accepted=True            
        )
        payment.save()
    service.payment_status = post_data['payment']
    service.status = post_data['service']
    service.save()
    return redirect('servicedetail', sid)
    

def serviceList(request):
    servicelist = Service.objects.all()
    service_list = True
    return render(request, "service_list.html", {"servicelist": servicelist, "service_list": service_list})

def serviceTypeList(request):
    servicetypes = ServiceType.objects.all()
    service_types = True
    return render(request, "service_type_list.html", {"servicetypes": servicetypes, "service_types": service_types})

def salesServices(request):
    services = Services.objects.all().order_by('-created_at')
    sales = True
    print(sales)
    return render(request, "sales_services.html", {"services": services, "sales": sales})

def accountsIndex(request):
    accounts = True
    users = DashboardUser.objects.all()
    total_service_price = 0
    total_payment_accepted = 0
    total_due = 0
    services = Services.objects.all()

    timeline = []
    sales = []
    for service in services:
        print(service.created_at)
        print(service.dateStamp())
        timeline.append(service.dateStamp())
        sales.append(service.price)
        total_service_price += service.price
        payments = ServicePayments.objects.filter(service__id=service.id)
        for payment in payments:
            if payment.accepted == True:
                total_payment_accepted += payment.amount
    total_due = total_service_price - total_payment_accepted
    return render(request, "accounts/index.html", 
                {"accounts": accounts,                 
                "users": users,
                "timeline" : json.dumps(timeline),
                "sales" : sales,
                "total_service_price": total_service_price,
                "total_payment_accepted": total_payment_accepted,
                "total_due": total_due})

def accountsDetail(request, aid):
    accounts = True
    user = DashboardUser.objects.get(id=aid)
    
    try:
        rank = UserRank.objects.get(user_id=aid)
    except:
        rank = False
    total_service_price = 0
    total_payment_accepted = 0
    total_due = 0
    services = Services.objects.filter(user__id=user.id)
    for service in services:
        total_service_price += service.price
        payments = ServicePayments.objects.filter(service__id=service.id)
        for payment in payments:
            if payment.accepted == True:
                total_payment_accepted += payment.amount
    total_due = total_service_price - total_payment_accepted
    return render(request, "accounts/detail.html", 
                {"accounts": accounts, 
                "user": user,
                "rank": rank,
                "services": services,
                "total_service_price": total_service_price,
                "total_payment_accepted": total_payment_accepted,
                "total_due": total_due})
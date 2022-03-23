from itertools import product
from pdb import post_mortem
from time import strftime
from django.db.models.fields import PositiveBigIntegerField
from django.http.response import ResponseHeaders
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
import json

from datetime import datetime, date
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncWeek
from pip import main

from .models import *

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
BDT_CONVERTER = 80.0


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
        services = Services.objects.all().order_by('-date')
        servicelist = Service.objects.order_by('title')
        servicetypes = ServiceType.objects.all()
        users = User.objects.all().exclude(is_superuser=True)
        users1 = DashboardUser.objects.all()
        return render(request, 'index.html', 
            {"data": data, "notices": notices, "services": services, "users": users1, 
                "servicelist": servicelist, "servicetypes": servicetypes, "home": home})
    else:
        req_user = DashboardUser.objects.get(user=user.id)
        if req_user.user_type == 'sales':
            try:
                data = ""
                notices = Notices.objects.all()
                services = Services.objects.filter(user__id=req_user.id).order_by('-date')
                servicelist = Service.objects.order_by('title')      
                info = DashboardUser.objects.get(user_id=request.user.id)
                rank = UserRank.objects.get(user_id=info.id)
                print(rank.title)
                return render(request, 'sales_dashboard.html', 
                    {"data": data, "notices": notices, "services": services, "info": info, "servicelist": servicelist, "rank": rank, "home": home})
            except:
                data = ""
                notices = Notices.objects.all()
                services = Services.objects.filter(user__id=req_user.id).order_by('-date')
                servicelist = Service.objects.order_by('title')         
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
    date_stat = "disabled"
    servicelist = Service.objects.order_by('title')
    servicetypes = ServiceType.objects.all()
    service_create = True
    users = DashboardUser.objects.all()
    today = date.today()
    today_date = today.strftime("%m/%d/%Y")

    if request.user.is_superuser:
        date_stat = ""
    
    try:
        info = DashboardUser.objects.get(user_id=request.user.id)
        rank = UserRank.objects.get(user_id=info.id)
        return render(request, 'service_create.html', {"data": data, "date_stat": date_stat, "date": today_date, "users":users, "servicelist": servicelist, "servicetypes": servicetypes, "info": info, "rank": rank, "service_create": service_create})
    except:
        return render(request, 'service_create.html', {"data": data, "date_stat": date_stat, "date": today_date, "users":users, "servicelist": servicelist, "servicetypes": servicetypes, "service_create": service_create})

def saveService(request):
    post_data = request.POST
    print(post_data)
    if request.user.is_superuser:
        dashboarduser = DashboardUser.objects.get(id=post_data['dashboarduser'])
        service_title = Service.objects.get(id=post_data['service'])
        service_type = ServiceType.objects.get(id=post_data['service_type'])
        date = post_data['date']
        print(date)
        print(type(date))
        date_obj = datetime.strptime(date, '%m/%d/%Y')
        print(date_obj.date())
        print(type(date_obj.date()))
        # print(isinstance(date, datetime.date))
        service = Services(
            user=dashboarduser,
            date=date_obj,
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
        service.status = "Pending"
        service.payment_status = "Due"
        service.save()
    else:        
        user = request.user
        dashboarduser = DashboardUser.objects.filter(user_id=user.id).last()
        service_title = Service.objects.get(id=post_data['service'])
        service_type = ServiceType.objects.get(id=post_data['service_type'])
        date = post_data['date']
        print(date)
        print(type(date))
        date_obj = datetime.strptime(date, '%m/%d/%Y')
        print(date_obj.date())
        print(type(date_obj.date()))
        service = Services(
            user=dashboarduser,
            date=date_obj,
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
        service.status = "Pending"
        service.payment_status = "Due"
        service.save()

    return redirect('/')

def serviceUpdate(request, sid):
    data = ""
    servicelist = Service.objects.order_by("title")
    servicetypes = ServiceType.objects.all()
    # service_create = True
    users = DashboardUser.objects.all()
    service = Services.objects.get(id=sid)
    today = date.today()
    today_date = today.strftime("%m/%d/%Y")
    try:
        info = DashboardUser.objects.get(user_id=request.user.id)
        rank = UserRank.objects.get(user_id=info.id)
        return render(request, 'service_update.html', {"data": data, "date": today_date, "service":service, "users":users, "servicelist": servicelist, "servicetypes": servicetypes, "info": info, "rank": rank})
    except:
        return render(request, 'service_update.html', {"data": data, "date": today_date, "service":service, "users":users, "servicelist": servicelist, "servicetypes": servicetypes})

def updateServiceValue(request,sid):
    post_data = request.POST
    date = post_data['date']
    print(date)
    print(type(date))
    date_obj = datetime.strptime(date, '%m/%d/%Y')
    print(date_obj.date())
    print(type(date_obj.date()))
    service_obj = Services.objects.get(id=sid)
    service_obj.title=post_data['title']
    service_obj.site_name=post_data['site_name']
    service_obj.site_url=post_data['site_url']
    service_obj.counter=post_data['counter']
    service_obj.ratio=post_data['ratio']
    service_obj.price=int(float(post_data['price']))
    service_obj.date = date_obj

    service_obj.save()
    return redirect('servicedetail', sid)

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
    print(service.status)
    print(service.payment_status)
    payments = ServicePayments.objects.filter(service__id=sid)
    remaining = service.price
    for payment in payments:
        if payment.accepted:
            paid += payment.amount
            remaining -= payment.amount


    if paid >= service.price:
        toPay = False
        # service.payment_status = "Received"
        # service.status = "Done"
    
    try:
        info = DashboardUser.objects.get(user_id=request.user.id)
        rank = UserRank.objects.get(user_id=info.id)
        return render(request, 'service_detail.html', 
                {"data": data, "service": service, "payments": payments, "paid": paid, "remaining": remaining, "toPay": toPay, "info": info, "rank": rank})        
    except:
        return render(request, 'service_detail.html', {"data": data, "service": service, "payments": payments, "paid": paid, "remaining": remaining, "toPay": toPay})

def acceptService(requset, sid):
    service = Services.objects.get(id=sid)
    service.accepted = True
    service.status = "Working"
    service.save()

    return redirect('servicedetail', sid)

def declineService(requset, sid):
    service = Services.objects.get(id=sid)
    service.delete()

    return redirect('salesservices')

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

def declinePayment(request, pid):
    payment = ServicePayments.objects.get(id=pid)
    service = payment.service
    payment.delete()

    return redirect('servicedetail', service.id)


def donePayment(request, sid):
    service = Services.objects.get(id=sid)
    service.payment_status = "Received"
    service.status = "Done"
    service.save()
    payments = ServicePayments.objects.filter(service__id=sid)
    if payments.exists():
        for pay in payments:
            pay.accepted = True
            pay.save()
        return redirect('servicedetail', sid)
    else:
        payment = ServicePayments(
            service = service,
            amount = service.price,
            link = "Auto Received",
            accepted=True,
        )
        payment.save()
        return redirect('servicedetail', sid)


    # try:
    #     print("inside try")

        
    #     print(payments)
    #     for pay in payments:
    #         pay.accepted = True
    #         pay.save()
    #     return redirect('servicedetail', sid)
    # except:
    #     print("inside exxcept")
    #     payment = ServicePayments(
    #         service = service,
    #         amount = service.price,
    #         link = "Auto Received",
    #         accepted=True,
    #     )
    #     payment.save()
    #     print(payment)
    #     return redirect('servicedetail', sid)

    

def fraudPayment(request, sid):
    service = Services.objects.get(id=sid)
    service.payment_status = "Fraud"
    service.status = "Failed"
    service.save()

    return redirect('servicedetail', sid)

def otherPayment(request, sid):
    service = Services.objects.get(id=sid)    
    post_data = request.POST
    if post_data['payment'] == "Received" or "NA":
        payments = ServicePayments.objects.filter(service__id=sid)
        if payments.exists():
            for pay in payments:
                pay.accepted = True
                pay.save()
        else:
            payment = ServicePayments(
                service = service,
                amount = service.price,
                link = "Auto Received",
                accepted=True,
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
    if request.user.is_superuser:
        services = Services.objects.all().order_by('-date')
    else:
        user = request.user
        dash_user = DashboardUser.objects.get(user=user.id)
        services = Services.objects.filter(user__id=dash_user.id).order_by('-date')
    sales = True
    print(sales)
    return render(request, "sales_services.html", {"services": services, "sales": sales})

def accountsIndex(request):
    accounts = True
    users = DashboardUser.objects.all()
    total_service_price = 0
    total_payment_accepted = 0
    total_due = 0
    timeline = []
    sales = []
    services = Services.objects.all()


    monthly_data = Services.objects.annotate(month = TruncMonth('date')).values('month').annotate(services=Count('id'), total=Sum('price')).order_by('month')

    for month in monthly_data:
        timeline.append(month['month'].strftime('%B'))
        sales.append(month['total'])
        print(month['month'].strftime('%B'), month['total'])

    print(monthly_data)


    for service in services:
        print(service.date)
        print(service.dateStamp())
        # timeline.append(service.dateStamp())
        # sales.append(service.price)
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
                "sale" : sales,
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
    services = Services.objects.filter(user__id=user.id).order_by('-date')
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


def searchResult(request):
    data = request.POST['search_key']
    results = Services.objects.filter(title__icontains=data)
    return render(request, "search_result.html", {"data": data, "results": results})

def monthlySales(request):
    sales_info = True
    total_service_price = 0
    total_payment_accepted = 0
    total_due = 0
    timeline = []
    sales = []
    services = Services.objects.all()

    data = []

    monthly_data = Services.objects.annotate(month = TruncMonth('date')).values('month').annotate(services=Count('id'), total=Sum('price')).order_by('month')

    for month in monthly_data:
        timeline.append(month['month'].strftime('%B'))
        sales.append(month['total'])
        sale_data = {
            "month": month['month'].strftime('%B'),
            "year": month['month'].strftime('%Y'),
            "mm": month['month'].strftime('%m'),
            "total": month['total'],
            "services": month['services']
            }
        data.append(sale_data)

    for service in services:
        total_service_price += service.price
        payments = ServicePayments.objects.filter(service__id=service.id)
        for payment in payments:
            if payment.accepted == True:
                total_payment_accepted += payment.amount
    total_due = total_service_price - total_payment_accepted
    return render(request, "accounts/monthly_sales.html",
                    {"sales_info": sales_info, 
                    "timeline": json.dumps(timeline), 
                    "sale": sales, 
                    "total_service_price": total_service_price,
                    "total_payment_accepted": total_payment_accepted,
                    "total_due": total_due,
                    "monthly_data": data})


def monthlySaleDetail(request, mm, yy):
    sales_info = True
    month = date(1900, mm, 1).strftime('%B')

    services1 = Services.objects.filter(date__year=yy,
                                        date__month=mm)

    services = Services.objects.filter(date__year=yy,
                                        date__month=mm).order_by('date')

    # print(services.count())

    # service_data = services.filter(payment_status="Received")
    service_data = services.filter(Q(payment_status="Received") | Q(payment_status="NA"))
    print(service_data.count())

    # print(services1)
    # print(services)

    user_list = (services1
            .values('user')
            .annotate(services=Count('user'), total=Sum('price'))
        )
    # print(user_list)

    monthly_filtered = []

    for data in user_list:
        user_id = data['user']
        user = DashboardUser.objects.get(id=user_id)
        user_services = service_data.filter(user_id=user_id)
        weekly_calc = user_services.annotate(week = TruncWeek('date')).values('week').annotate(services=Count('id'), total=Sum('price')).order_by('week')
        # print("weekly calculator")
        # print(weekly_calc)
        weekly_data = []
        total = 0
        total_earned = 0
        total_earned_bdt = 0
        earned = 0
        earned_bdt = 0
        # print(len(weekly_calc))
        for data in weekly_calc:
            total += data['total']
            if data['total'] > CAP_0 and data['total'] <CAP_1:
                earned = data['total'] * TIER_0_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
                # total_earned += earned
                # total_earned_bdt += earned_bdt
            elif data['total'] > CAP_1 and data['total'] <CAP_2:
                earned = data['total'] * TIER_1_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
                # total_earned += earned
                # total_earned_bdt += earned_bdt
            elif data['total'] > CAP_2 and data['total'] <CAP_3:
                earned = data['total'] * TIER_2_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
                # total_earned += earned
                # total_earned_bdt += earned_bdt
            elif data['total'] > CAP_3 and data['total'] <CAP_4:
                earned = data['total'] * TIER_3_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
                # total_earned += earned
                # total_earned_bdt += earned_bdt
            elif data['total'] >= CAP_4:
                earned = data['total'] * TIER_4_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
                # total_earned += earned
                # total_earned_bdt += earned_bdt
            total_earned += earned
            total_earned_bdt += earned_bdt
            weeks = {
                "services": data['services'],
                "total": data['total'],
                "earned": earned,
                "earned_bdt": earned_bdt
            }
            weekly_data.append(weeks)
        
        if len(weekly_calc) > 4:
            idx = 4
            main_data = weekly_data[:idx]
            remaining_data = weekly_data[idx:]

            for data in remaining_data:
                obj = main_data[idx-1]
                obj['services'] += data['services']
                obj['total'] += data['total']
                obj['earned'] += data['earned']
                obj['earned_bdt'] += data['earned_bdt']

            weekly_data = main_data

        elif len(weekly_calc) < 4:
            for x in range(0, 4-len(weekly_calc)):
                weeks = {
                    "services": 0,
                    "total": 0,
                    "earned": 0,
                    "earned_bdt": 0
                }
                weekly_data.append(weeks)
            

        

        filtered_row = {
                "user": user,
                "service_count": data['services'],
                "total": total,
                "total_earned": total_earned,
                "total_earned_bdt": total_earned_bdt,
                "week": weekly_data,                
            }
        monthly_filtered.append(filtered_row)
    # print(monthly_filtered)
    # weekly_data = services.annotate(week = TruncWeek('date')).values('week').annotate(services=Count('id'), total=Sum('price'))


    return render(request, "accounts/monthly_sale_detail.html", 
                    {"sales_info": sales_info,
                        "month": month,
                        "year": yy,
                        "sale_data": monthly_filtered})

def clientIndex(request):
    data = ""
    products = serviceProduct.objects.all()
    return render(request, "client/index.html", {"data": data, "products": products})

def clientServiceDetail(request):
    data = ""
    return render(request, "client/detail.html", {"data": data})

def clientOrders(request):
    data = ""
    return render(request, "client/orders.html", {"data": data})

def allOrders(request):
    data = ""
    return render(request, "orders.html", {"data": data})

def orderDetail(request):
    data = ""
    return render(request, "client/order_detail.html", {"data": data})

def createProduct(request):
    data = ""
    categories = productCategory.objects.all()
    return render(request, "clientdash/create_product.html", {"data": data, "categories": categories})

def saveProduct(request):
    data = ""
    post_data = request.POST
    cat_id = post_data['category']
    category = productCategory.objects.get(id=cat_id)

    product = serviceProduct(
        name = post_data['name'],
        ptype = post_data['type'],
        category = category,
        description = post_data['description'],
        measurement = post_data['measurement'],
        price = post_data['price']
    )

    product.save()
    return redirect('productlist')

def saveCategory(request):
    post_data = request.POST

    category = productCategory(
        name = post_data['name']
    )

    category.save()

    return redirect('createproduct')

def productList(request):
    data = ""
    products = serviceProduct.objects.all()
    inactive = "inactive"
    active = "active"
    return render(request, "clientdash/product_list.html", {"data": data, "products": products, "inactive": inactive, "active": active})

def productAct(request, pid, act):
    product = serviceProduct.objects.get(id=pid)
    if act == "active":
        product.status = True
        product.save()
    elif act == "inactive":
        product.status = False
        product.save()

    return redirect('productlist')

def clientList(request):
    data = ""
    return render(request, "clientdash/client_list.html", {"data": data})

def orderList(request):
    data = ""
    return render(request, "clientdash/order_list.html", {"data": data})
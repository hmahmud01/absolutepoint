from itertools import product
from pdb import post_mortem
from time import strftime
from django.db.models.fields import PositiveBigIntegerField
from django.http.response import ResponseHeaders, JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
import json
import requests
# from datetime import datetime, date
import datetime
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncWeek
from pip import main

from .models import *
from .utils import cartData

BASE_SALARY = 10000

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

JAN = 31
FEB = 28
MAR = 31
APR = 30
MAY = 31
JUN = 30
JUL = 31
AUG = 31
SEP = 30
OCT = 31
NOV = 30
DEC = 31

HOURS_DELTA = 6


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
        current_day = datetime.date.today()
        month = current_day.month
        services_user = Services.objects.filter(user__id=req_user.id)
        service_data = services_user.filter(Q(payment_status="Received") | Q(payment_status="NA"))
        services = service_data.filter(date__month=month)
        weekly_data = services.annotate(week = TruncWeek('date')).values('week').annotate(services=Count('id'), total=Sum('price')).order_by('week')
        timeline = [1, 2, 3, 4]
        sale = []

        for data in weekly_data:
            sale.append(data['total'])

        length = len(weekly_data)

        if length > 4 :
            idx = 4
            main_sale = sale[:idx]
            remain_sale = sale[idx:]

            for data in remain_sale:
                main_sale[idx-1] += data
            
            sale = main_sale
        elif length < 4:
            for x in range(0, 4-length):
                sale.append(0.0)
        
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
                    {"timeline": timeline, "sale": sale, "data": data, "notices": notices, "services": services, "info": info, "servicelist": servicelist, "rank": rank, "home": home})
            except:
                data = ""
                notices = Notices.objects.all()
                services = Services.objects.filter(user__id=req_user.id).order_by('-date')
                servicelist = Service.objects.order_by('title')         
                info = DashboardUser.objects.get(user_id=request.user.id)
                return render(request, 'sales_dashboard.html', 
                    {"timeline": timeline, "sale": sale, "data": data, "notices": notices, "services": services, "info": info, "servicelist": servicelist, "home": home})
            

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

def duplicateService(request):
    return render(request, 'service_create_duplicate.html')

def serviceCreate(request):
    data = ""
    date_stat = "disabled"
    servicelist = Service.objects.order_by('title')
    servicetypes = ServiceType.objects.all()
    service_create = True
    users = DashboardUser.objects.all()
    today = datetime.date.today()
    timedate = datetime.datetime.now()
    updated_timedate = datetime.timedelta(hours=HOURS_DELTA)
    updated_time = timedate + updated_timedate

    today_updated = updated_time.date()

    # print(today_now)
    today_date = today_updated.strftime("%m/%d/%Y")

    if request.user.is_superuser:
        date_stat = ""
    
    try:
        info = DashboardUser.objects.get(user_id=request.user.id)
        rank = UserRank.objects.get(user_id=info.id)
        return render(request, 'service_create.html', {"data": data, "date_stat": date_stat, "date": today_date, "users":users, "servicelist": servicelist, "servicetypes": servicetypes, "info": info, "rank": rank, "service_create": service_create})
    except:
        return render(request, 'service_create.html', {"data": data, "date_stat": date_stat, "date": today_date, "users":users, "servicelist": servicelist, "servicetypes": servicetypes, "service_create": service_create})

def saveService(request):
    check = True
    post_data = request.POST
    if request.user.is_superuser:
        dashboarduser = DashboardUser.objects.get(id=post_data['dashboarduser'])
        service_title = Service.objects.get(id=post_data['service'])
        service_type = ServiceType.objects.get(id=post_data['service_type'])
        date = post_data['date']
        date_obj = datetime.datetime.strptime(date, '%m/%d/%Y')

        services_objects = Services.objects.filter(date=date_obj)
        for obj in services_objects:
            if obj.site_url == post_data['site_url']:
                check = False
                break
            else:
                check = True

        if check:
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
        else:
            return redirect('duplicateservice')
        
    else:        
        user = request.user
        dashboarduser = DashboardUser.objects.filter(user_id=user.id).last()
        service_title = Service.objects.get(id=post_data['service'])
        service_type = ServiceType.objects.get(id=post_data['service_type'])
        date = post_data['date']
        date_obj = datetime.datetime.strptime(date, '%m/%d/%Y')

        services_objects = Services.objects.filter(date=date_obj)
        for obj in services_objects:
            if obj.site_url == post_data['site_url']:
                check = False
                break
            else:
                check = True
        if check:
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
        else:
            return redirect('duplicateservice')
    # return redirect('servicecreate')

# TODO 
# DO an update function for service to create commision limit based on limited sales of the
# connected service only and calculate that on the salary and accounts sheet for payment to 
# sales executive.

def updateServiceBonus(request):
    post_data = request.POST
    service = Service.objects.get(id=post_data['service'])
    service.comm_status = True
    service.cap = post_data['cap']
    service.commission = post_data['commission']
    service.save()
    return redirect('servicelist')

def serviceBonus(request, sid):
    service = Services.objects.get(id=sid)
    post_data = request.POST
    service.comm_status = True
    service.commission = post_data['commission']
    rate = post_data['commission']
    service.save()
    service.comm_amount = float(service.price) * float(rate) / 100
    service.save()
    return redirect('servicedetail', sid)

def removeServiceBonus(request, sid):
    service = Services.objects.get(id=sid)
    service.comm_status = False
    service.commission = 0
    service.comm_amount = 0
    service.save()
    return redirect('servicedetail', sid)

def seasonBonus(request):
    data= SalesBonus.objects.all()

    return render(request, 'accounts/season_bonus.html', {"datas": data})

def addSeasonBonus(request):
    users = DashboardUser.objects.all()
    today = datetime.date.today()
    today_date = today.strftime("%m/%d/%Y")

    return render(request, 'accounts/season_bonus_add.html', {"date": today_date, "users": users})

def submitseasonbonus(request):
    post_data = request.POST
    user = DashboardUser.objects.get(id=post_data['user'])
    date = post_data['date']
    date_obj = datetime.datetime.strptime(date, '%m/%d/%Y')
    salebonus = SalesBonus(
        emp = user,
        amount = post_data['bonus'],
        detail = post_data['remarks'],
        date = date_obj
    )

    salebonus.save()
    return redirect('seasonbonus')

def removeSeasonBonus(request, bid):
    bonusObj = SalesBonus.objects.get(id=bid)
    bonusObj.delete()

    return redirect('seasonbonus')    


def serviceUpdate(request, sid):
    data = ""
    servicelist = Service.objects.order_by("title")
    servicetypes = ServiceType.objects.all()
    users = DashboardUser.objects.all()
    service = Services.objects.get(id=sid)
    today = datetime.date.today()
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
    date_obj = datetime.datetime.strptime(date, '%m/%d/%Y')
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

def updateServiceType(request):
    post_data = request.POST
    serviceType = ServiceType.objects.get(id=post_data['type'])
    serviceType.title = post_data['title']
    serviceType.save()
    return redirect('/')

def removeUser(request):
    post_data = request.POST
    dash_user = DashboardUser.objects.get(id=post_data['user'])
    user = User.objects.get(id=dash_user.user.id)
    user.delete()
    dash_user.delete()
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
                amount = 0,
                link = "Auto Received",
                accepted=True,
            )
            payment.save()
    service.payment_status = post_data['payment']
    service.status = post_data['service']
    service.save()

    return redirect('servicedetail', sid)
    

def serviceList(request):
    servicelist = Service.objects.all().order_by('title')
    service_list = True
    bonuslist = servicelist.filter(comm_status=True)
    return render(request, "service_list.html", {"servicelist": servicelist, "service_list": service_list, 'bonuslist': bonuslist})

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

    service_data = services.filter(Q(payment_status="Received") | Q(payment_status="NA"))

    data = []

    monthly_data = service_data.annotate(month = TruncMonth('date')).values('month').annotate(services=Count('id'), total=Sum('price')).order_by('month')

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

    for service in service_data:
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
    month = datetime.date(1900, mm, 1).strftime('%B')

    services1 = Services.objects.filter(date__year=yy,
                                        date__month=mm)

    services = Services.objects.filter(date__year=yy,
                                        date__month=mm).order_by('date')


    service_data = services.filter(Q(payment_status="Received") | Q(payment_status="NA"))


    user_list = (services1
            .values('user')
            .annotate(services=Count('user'), total=Sum('price'))
        )

    monthly_filtered = []
    monthly_custom = []
    for data in user_list:
        user_id = data['user']  
        user = DashboardUser.objects.get(id=user_id)
        user_services = service_data.filter(user_id=user_id)
        dummy_services = user_services
        user_services = user_services.exclude(comm_status=True)
        
        weekly_calc = user_services.annotate(week = TruncWeek('date')).values('week').annotate(services=Count('id'), total=Sum('price')).order_by('week')

        service_custom = 0
        service_bonus = 0
        service_bonus_bdt = 0
        cap = 0
        commission = 0
        total = 0
        services_bonus_data = service_data.filter(service__comm_status=True)
        bonus_data = services_bonus_data.values('service').annotate(pieces=Count('service'), total=Sum('price')).order_by()

        services_custom_comm = dummy_services.filter(comm_status=True)
        for custom in services_custom_comm:
            service_custom += custom.price
            service_bonus += custom.comm_amount
        
        service_bonus_bdt = service_bonus * BDT_CONVERTER

        season_bonus = 0
        seasonal_bonus = SalesBonus.objects.filter(emp_id=user_id).filter(date__month=mm)
        for season in seasonal_bonus:
            season_bonus += season.amount


        tier_bonus = 0
        tier_bonus_bdt = 0
        bonus_cap = 0
        for serv in user_services:
            bonus_cap += serv.price
        if bonus_cap >= CAP_4:
            tier_bonus = bonus_cap * TIER_4_PERCENT / 100
            tier_bonus_bdt = tier_bonus * BDT_CONVERTER

        week_1 = 0
        week_2 = 0
        week_3 = 0
        week_4 = 0
        week_1_data = user_services.filter(date__day__gte=1, date__day__lte=7)
        week_2_data = user_services.filter(date__day__gte=8, date__day__lte=14)
        week_3_data = user_services.filter(date__day__gte=15, date__day__lte=21)
        week_4_data = user_services.filter(date__day__gte=22, date__day__lte=31)


        for data in week_1_data:
            week_1 += data.price

        for data in week_2_data:
            week_2 += data.price
        
        for data in week_3_data:
            week_3 += data.price

        for data in week_4_data:
            week_4 += data.price


        weekly_total = []
        weekly_total.append(week_1)
        weekly_total.append(week_2)
        weekly_total.append(week_3)
        weekly_total.append(week_4)

        weekly_data = []
        total = 0
        total_earned = 0
        total_earned_bdt = 0
        earned = 0
        earned_bdt = 0
        for data in weekly_total:
            total += data
            if data == 0:
                earned = 0
                earned_bdt = 0
                total_earned = 0
                total_earned_bdt = 0
            elif data > CAP_0 and data <CAP_1:
                earned = data * TIER_0_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
            elif data > CAP_1 and data <CAP_2:
                earned = data * TIER_1_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
            elif data > CAP_2 and data <CAP_3:
                earned = data * TIER_2_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
            elif data > CAP_3:
                earned = data * TIER_3_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
            
            weeks = {
                "total": data,
                "earned": earned,
                "earned_bdt": earned_bdt
            }
            weekly_data.append(weeks)
        
        for data in weekly_data:
            total_earned += data['earned']
            total_earned_bdt += data['earned_bdt']
        total += service_custom
        total_earned += tier_bonus
        total_earned += service_bonus
        total_earned_bdt += tier_bonus_bdt
        total_earned_bdt += service_bonus_bdt
        total_earned_bdt += season_bonus

        total_earned_bdt += BASE_SALARY
        filtered_row = {
                "user": user,
                "total": total,
                "total_earned": total_earned,
                "total_earned_bdt": total_earned_bdt,
                "base_salary": BASE_SALARY,
                "week": weekly_data,        
                "tier_bonus": tier_bonus,
                "tier_bonus_bdt": tier_bonus_bdt,
                "service_custom": service_custom,
                "service_bonus": service_bonus,
                "service_bonus_bdt": service_bonus_bdt,
                "season_bonus": season_bonus, 
            }
        monthly_custom.append(filtered_row)


    return render(request, "accounts/monthly_sale_detail.html", 
                    {"sales_info": sales_info,
                        "month": month,
                        "year": yy,
                        "sale_data": monthly_custom})

def salesExecutiveSalary(request):
    user_id = request.user.id
    dash_user = DashboardUser.objects.get(user_id=user_id)

    services = Services.objects.filter(user_id=dash_user.id)
    service_data = services.filter(Q(payment_status="Received") | Q(payment_status="NA"))

    salary_row = []
    salary_custom = []
    monthly_services = service_data.annotate(month = TruncMonth('date')).values('month').annotate(services=Count('id'), total=Sum('price')).order_by('month')
    
    for data in monthly_services:
        mm = data['month'].month
        month_data = datetime.date(2022, mm, 1).strftime('%B')
        service_month = service_data.filter(date__month=mm)
        services_custom_comm = service_month.filter(comm_status=True)
        service_month = service_month.exclude(comm_status=True)

        service_custom = 0
        service_bonus = 0
        service_bonus_bdt = 0
        cap = 0
        commission = 0
        total = 0
        # services_bonus_data = service_month.filter(service__comm_status=True)
        # bonus_data = services_bonus_data.values('service').annotate(pieces=Count('service'), total=Sum('price')).order_by()


        # for bonus_service in bonus_data:
        #     service_id = bonus_service['service']
        #     total = bonus_service['total']
        #     service = Service.objects.get(id=service_id)
        #     cap = service.cap
        #     commission = service.commission

        #     if total >= cap:
        #         earned = total * commission / 100
        #         service_bonus += earned
        #         service_bonus_bdt += earned * BDT_CONVERTER

        for custom in services_custom_comm:
            service_custom += custom.price
            service_bonus += custom.comm_amount
        
        service_bonus_bdt = service_bonus * BDT_CONVERTER

        season_bonus = 0
        seasonal_bonus = SalesBonus.objects.filter(emp_id=dash_user.id).filter(date__month=mm)

        for season in seasonal_bonus:
            season_bonus += season.amount



        tier_bonus = 0
        tier_bonus_bdt = 0
        bonus_cap = 0
        for serv in service_month:
            bonus_cap += serv.price
        if bonus_cap >= CAP_4:
            tier_bonus = bonus_cap * TIER_4_PERCENT / 100
            tier_bonus_bdt = tier_bonus * BDT_CONVERTER

        week_1 = 0
        week_2 = 0
        week_3 = 0
        week_4 = 0
        week_1_data = service_month.filter(date__day__gte=1, date__day__lte=7)
        week_2_data = service_month.filter(date__day__gte=8, date__day__lte=14)
        week_3_data = service_month.filter(date__day__gte=15, date__day__lte=21)
        week_4_data = service_month.filter(date__day__gte=22, date__day__lte=31)

        for data in week_1_data:
            week_1 += data.price

        for data in week_2_data:
            week_2 += data.price
        
        for data in week_3_data:
            week_3 += data.price

        for data in week_4_data:
            week_4 += data.price

        weekly_total = []
        weekly_total.append(week_1)
        weekly_total.append(week_2)
        weekly_total.append(week_3)
        weekly_total.append(week_4)

        weekly_data = []
        total = 0
        total_earned = 0
        total_earned_bdt = 0
        earned = 0
        earned_bdt = 0
        for data in weekly_total:
            total += data
            if data == 0:
                earned = 0
                earned_bdt = 0
                total_earned = 0
                total_earned_bdt = 0
            elif data > CAP_0 and data <CAP_1:
                earned = data * TIER_0_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
            elif data > CAP_1 and data <CAP_2:
                earned = data * TIER_1_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
            elif data > CAP_2 and data <CAP_3:
                earned = data * TIER_2_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
            elif data > CAP_3:
                earned = data * TIER_3_PERCENT / 100
                earned_bdt = earned * BDT_CONVERTER
            
            weeks = {
                "total": data,
                "earned": earned,
                "earned_bdt": earned_bdt
            }
            weekly_data.append(weeks)
        
        for data in weekly_data:
            total_earned += data['earned']
            total_earned_bdt += data['earned_bdt']
        
        total += service_custom
        total_earned += tier_bonus
        total_earned += service_bonus
        total_earned_bdt += tier_bonus_bdt
        total_earned_bdt += season_bonus
        total_earned_bdt += service_bonus_bdt
        total_earned_bdt += BASE_SALARY 

        filtered_row = {
                "month": month_data,
                "total": total,
                "total_earned": total_earned,
                "total_earned_bdt": total_earned_bdt,
                "base_salary": BASE_SALARY,
                "week": weekly_data,    
                "tier_bonus": tier_bonus,
                "tier_bonus_bdt": tier_bonus_bdt,
                "service_custom": service_custom,
                "service_bonus": service_bonus,
                "service_bonus_bdt": service_bonus_bdt,
                "season_bonus": season_bonus           
            }
        salary_row.append(filtered_row)

    return render(request, "accounts/sales_person.html", {"salary_row": salary_row})


# CLIENT AREA
def clientIndex(request):
    data = ""
    products = serviceProduct.objects.all()
    return render(request, "client/index.html", {"data": data, "products": products})

def clientServiceDetail(request, pid):
    data = ""
    product = serviceProduct.objects.get(id=pid)
    variables = variableProductPrice.objects.filter(product_id=pid)
    return render(request, "client/detail.html", {"data": data, "product": product, "variables": variables})

def clientOrders(request):
    data = ""
    return render(request, "client/orders.html", {"data": data})

def allOrders(request):
    data = ""
    return render(request, "orders.html", {"data": data})

def orderDetail(request):
    data = ""
    return render(request, "client/order_detail.html", {"data": data})

# CLIENT DASHBOARD

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

def productDetail(request, pid):
    data = ""
    product = serviceProduct.objects.get(id=pid)
    inactive = "inactive"
    active = "active"
    variables = variableProductPrice.objects.filter(product_id=pid)
    return render(request, "clientdash/product_detail.html", {"product": product, "inactive": inactive, "active": active, "variables": variables})

def saveVariablePrice(request):
    data = ""
    post_data = request.POST
    product = serviceProduct.objects.get(id=post_data['pid'])
    variable = variableProductPrice(
        product=product,
        measurement=post_data['measurement'],
        price=post_data['price']
    )
    variable.save()
    return redirect('productdetail', post_data['pid'])

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
    orders = Order.objects.all()
    return render(request, "clientdash/order_list.html", {"data": data, "orders": orders})

def orderDetailDash(request, oid):
    data = ""
    order = Order.objects.get(id=oid)
    orderItems = OrderItems.objects.filter(order_id=oid)
    context = {'items': orderItems, 'order':order}
    return render(request, "clientdash/order_detail.html", context)


def updateItem(request):
    data = json.loads(request.body)
    print(data)
    # {'productId': '1', 'action': 'add', 'price': '2'}
    productId = data['productId']
    action = data['action']
    price = data['price']

    customer = request.user.username
    product = serviceProduct.objects.get(id=productId)
    variance  = variableProductPrice.objects.get(id=price)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItems.objects.get_or_create(order=order, product=product, variance=variance)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    print(orderItem)

    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item Was Added', safe=False)

def cart(request):
    data = cartData(request)
    print(data)
    # {'cartItems': 1, 'order': <Order: 1>, 'items': <QuerySet [<OrderItems: OrderItems object (1)>]>}
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order':order, 'cartItems': cartItems}
    return render(request, "client/cart.html", context)

def checkout(request, oid):
    data = ""
    params = {
        "access_key": "e9bca0873fefe06bb0145b67feb8ec24"
        }
    response = requests.get('http://api.coinlayer.com/live', params=params)
    
    crypto_data = response.json()
    rates = crypto_data['rates']
    
    order = Order.objects.get(id=oid)
    order_items = OrderItems.objects.filter(order_id=oid)

        
    return render(request, "client/checkout.html", {"data": data, "rates": rates, 'order': order, 'order_items': order_items})


# <QueryDict: {'csrfmiddlewaretoken': ['Ka4Nh9QauQ361lj7sH5F09KVFkGptdqV8IUl8IgoDvbUOBvM5Yi25xqXx7tM0xwz'], 
# 'order': ['2'], 'firstname': ['Hasan'], 'lastname': ['Mahmud'], 'username': ['hmahmud01'], 'email': ['hmahmud01@example.com'], 
# 'address': ['Shantinagar'], 'address2': [''], 'country': ['Bangladesh'], 'state': ['Dhaka'], 'zipcode': ['1217'], 
# 'credit_type': ['on'], 'currency': ['{"AMB" : "0.009838"}']}>
def processOrder(request):
    data = ""
    post_data = request.POST
    order = Order.objects.get(id=post_data['order'])
    currency = json.loads(post_data['currency'])

    currency_key = list(currency.keys())[0]
    currency_value = float(list(currency.values())[0])

    order.complete = True
    order.save()

    billing = Billing(
        order = order,
        firstname = post_data['firstname'],
        lastname = post_data['lastname'],
        username = post_data['username'],
        email = post_data['email'],
        address = post_data['address'],
        address2 = post_data['address2'],
        country = post_data['country'],
        state = post_data['state'],
        zipcode = post_data['zipcode']
    )

    billing.save()

    payment = Payment(
        order = order,
        credit_type = post_data['credit_type'],
        currency_key = currency_key,
        currency_value = currency_value,
        total = order.get_cart_total
    )

    payment.save()

    return redirect('clientorders')

def createPortfolio(request):
    users = DashboardUser.objects.all()

    return render(request, "clientdash/create_portfolio.html", {"users": users})



# <QueryDict: {'csrfmiddlewaretoken': ['RlLYyo0LFMCGHxog1xUuiLZWz9hV90FNFCDM9GSAtpRiX3tvUJ4jsVjTfjNColIx'], 
# 'title': ['titl'], 'description': ['https://furniturefm.com'], 'contributors': ['1', '2']}>

# <MultiValueDict: {'thumb_image': [<TemporaryUploadedFile: wallpaper1_large.jpg (image/jpeg)>], 
# 'image': [<TemporaryUploadedFile: wallpaper1_large.jpg (image/jpeg)>, 
# <TemporaryUploadedFile: wallpaper1_large.png (image/png)>, <TemporaryUploadedFile: wallpaper2_large.jpg (image/jpeg)>]}>
def savePortfolio(request):
    post_data = request.POST
    file_data = request.FILES
    
    portfolio = Portfolio(
        title = post_data['title'],
        description = post_data['description'],
        thumb = file_data['thumb_image']
    )

    portfolio.save()

    contributors = post_data.getlist('contributors')

    for contributor in contributors:
        dashuser = DashboardUser.objects.get(id=contributor)
        keeper = PortfolioContributors(
            portfolio = portfolio,
            contributor = dashuser,
        )
        keeper.save()

    images = file_data.getlist('image')

    for image in images:
        proof = PortfolioProves(
            portfolio = portfolio,
            image = image
        )
        proof.save()
    
    return redirect('createportfolio')

def portfolio(request):
    portfolios = Portfolio.objects.all()

    return render(request, "client/portfolio.html", {"portfolios": portfolios})

def portfolioDetail(request, pid):
    portfolio = Portfolio.objects.get(id=pid)
    contributors = PortfolioContributors.objects.filter(portfolio_id=pid)
    proofs = PortfolioProves.objects.filter(portfolio_id=pid)

    return render(request, "client/portfolio_detail.html", {"portfolio": portfolio, "contributors": contributors, 'proofs': proofs})

def people(request):
    people = DashboardUser.objects.all()

    return render(request, "client/people.html", {"people": people})

def peopleDetail(request, pid):
    dashuser = DashboardUser.objects.get(id=pid)
    portfolios = PortfolioContributors.objects.filter(contributor_id=pid)

    return render(request, "client/people_detail.html", {"dashuser": dashuser, "portfolios": portfolios})
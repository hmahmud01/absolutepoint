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
from django.db.models import Count, Sum, Min
from django.db.models.functions import TruncMonth, TruncWeek
from pip import main
import stripe
from .models import *
from .utils import cartData
import random

stripe.api_key = "sk_test_51HhxVlEfJWhMuLjgUFtwqRpA9iGwTip8o2QuIq7BwYzbBysGhQCLXCt8TNZZMF4zcSUAhhfR0axTQKHEuMorCilV009353SShi"

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

# sount = 0
# tcount = 0

# cat_fb = 0
# cat_it= 0
# cat_yt = 0
# cat_tt = 0
# cat_tw = 0
# cat_tg = 0


scount = Services.objects.filter(accepted=False).count()
tcount = Ticket.objects.filter(seen=False).count()

cat_fb = productCategory.objects.get(name="Facebook Services").id
cat_it = productCategory.objects.get(name="Instagram Services").id
cat_yt = productCategory.objects.get(name="Youtube Services").id
cat_tt = productCategory.objects.get(name="Tiktok Services").id
cat_tw = productCategory.objects.get(name="Twitter Services").id
cat_tg = productCategory.objects.get(name="Telegram Services").id


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
            return redirect('home')

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
        # subject = 'Welcome to Absolute Point'
        # message = f'Hi {dashboardUser.username}, Your Account has been Created please login to the system with your email and password.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [dashboardUser.email, ]
        # send_mail( subject, message, email_from, recipient_list )
        dashboardUser.save()

        user_rank = UserRank(
            user=dashboardUser,
            title="NOOB",
            tier=0,
            sale_percent=5.0,
            current_earn=0.0
        )
        user_rank.save()
        return redirect('home')

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
    return redirect('home')

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
    return redirect('home')

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
        scount = Services.objects.filter(accepted=False).count()
        tcount = Ticket.objects.filter(seen=False).count()
        new_orders = Order.objects.filter(new_order=True).count()
        print(tcount)
        print(scount)
        print(new_orders)
        data = ""        
        notices = Notices.objects.all()
        services = Services.objects.all().order_by('-date')
        servicelist = Service.objects.order_by('title')
        servicetypes = ServiceType.objects.all()
        users = User.objects.all().exclude(is_superuser=True)
        users1 = DashboardUser.objects.all()    
        return render(request, 'index.html', 
            {"data": data, "notices": notices, "services": services, "users": users1, 
                "servicelist": servicelist, "servicetypes": servicetypes, "home": home, "tcount": tcount, "scount": scount, "new_orders": new_orders})
    else:
        try:
            req_user = AppUser.objects.get(user=user.id)
            return redirect('/')   
        except:
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
    return render(request, 'notice_create.html', {"data": data, "note_create": note_create, "tcount": tcount, "scount": scount})

def saveNotice(request):
    post_data = request.POST
    notice = Notices(
        title=post_data['title'],
        category=post_data['category'],
        description=post_data['description'],
        validity=post_data['validity']
    )

    notice.save()
    return redirect('home')

def noticeDetail(request, nid):
    data = ""
    notice = Notices.objects.get(id=nid)
    return render(request, 'notice_detail.html', {"data": data, "notice": notice, "tcount": tcount, "scount": scount})

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

    today_date = today_updated.strftime("%m/%d/%Y")

    if request.user.is_superuser:
        date_stat = ""
    
    try:
        info = DashboardUser.objects.get(user_id=request.user.id)
        rank = UserRank.objects.get(user_id=info.id)
        return render(request, 'service_create.html', {"data": data, "date_stat": date_stat, "date": today_date, "users":users, "servicelist": servicelist, "servicetypes": servicetypes, "info": info, "rank": rank, "service_create": service_create, "tcount": tcount, "scount": scount})
    except:
        return render(request, 'service_create.html', {"data": data, "date_stat": date_stat, "date": today_date, "users":users, "servicelist": servicelist, "servicetypes": servicetypes, "service_create": service_create, "tcount": tcount, "scount": scount})

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
            return redirect('home')
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

            return redirect('home')
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
    return redirect('home')

def removeServiceList(request, sid):
    service = Service.objects.get(id=sid)
    service.delete()

    return redirect('home')

def updateServiceList(request):
    post_data = request.POST
    service = Service.objects.get(id=post_data['service'])
    service.quantity = post_data['quantity']
    service.price = post_data['price']
    service.save()
    return redirect('home')

def updateServiceType(request):
    post_data = request.POST
    serviceType = ServiceType.objects.get(id=post_data['type'])
    serviceType.title = post_data['title']
    serviceType.save()
    return redirect('home')

def removeUser(request):
    post_data = request.POST
    dash_user = DashboardUser.objects.get(id=post_data['user'])
    user = User.objects.get(id=dash_user.user.id)
    user.delete()
    dash_user.delete()
    return redirect('home')

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
    return redirect('home')
    
def removeServiceTypeList(request, sid):
    service_type = ServiceType.objects.get(id=sid)
    service_type.delete()

    return redirect('home')

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
    items = []
    if request.user.is_superuser:
        status = ""
        services = Services.objects.all().order_by('-date')
        for service in services:
            payments = ServicePayments.objects.filter(service__id=service.id)
            if payments:
                for payment in payments:
                    if payment.accepted == False:
                        status = "New Payment"
                    else:
                        status = "No New Payment"
                    
                    obj = {
                        'service': service,
                        'status': status
                    }
            else:
                status = "No Payment"
                obj = {
                    'service': service,
                    'status': status
                }

            items.append(obj)      
    else:
        user = request.user
        dash_user = DashboardUser.objects.get(user=user.id)
        services = Services.objects.filter(user__id=dash_user.id).order_by('-date')
        for service in services:
            payments = ServicePayments.objects.filter(service__id=service.id)
            if payments:
                for payment in payments:
                    if payment.accepted == False:
                        status = "New Payment"
                    else:
                        status = "No New Payment"
                    
                    obj = {
                        'service': service,
                        'status': status
                    }
            else:
                status = "No Payment"
                obj = {
                    'service': service,
                    'status': status
                }

            items.append(obj)
    sales = True
    print(sales)
    print(items)
    return render(request, "sales_services.html", {"services": services, "items": items, "sales": sales, "tcount": tcount, "scount": scount})

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
    products = serviceProduct.objects.all().exclude(category__name="Marketing").exclude(category__name="Facebook Services").exclude(category__name="Instagram Services").exclude(category__name="Youtube Services").exclude(category__name="Tiktok Services").exclude(category__name="Twitter Services").exclude(category__name="Telegram Services").filter(status=True)[:8]
    items = []
    marketing = serviceProduct.objects.filter(category__name="Marketing Services")
    facebook = serviceProduct.objects.filter(category__name="Facebook Services")
    instagram = serviceProduct.objects.filter(category__name="Instagram Services")
    youtube = serviceProduct.objects.filter(category__name="Youtube Services")
    tiktok = serviceProduct.objects.filter(category__name="Tiktok Services")
    twitter = serviceProduct.objects.filter(category__name="Twitter Services")
    telegram = serviceProduct.objects.filter(category__name="Telegram Services")

    for prod in products:
        variable = variableProductPrice.objects.filter(product__id=prod.id).order_by('price')

        try:
            product = {
                'product': prod,
                'price': variable.first().price
            }

            items.append(product)
        except:
            product = {
                'product': prod,
                'price': 0
            }

            items.append(product)

    cat_fb = productCategory.objects.get(name="Facebook Services").id
    cat_it = productCategory.objects.get(name="Instagram Services").id
    cat_yt = productCategory.objects.get(name="Youtube Services").id
    cat_tt = productCategory.objects.get(name="Tiktok Services").id
    cat_tw = productCategory.objects.get(name="Twitter Services").id
    cat_tg = productCategory.objects.get(name="Telegram Services").id

    data = cartData(request)
    order = data['order']

    reviews = Review.objects.filter(status=True)

    review_items = []

    for review in reviews:
        user = review.user
        if user is None:
            username = "Anonymous"
            data = {
                "review" : review,
                "username" : username
            }
        else:
            try:
                app_user = AppUser.objects.get(user_id=user.id)
                username = app_user.fname + " " + app_user.lname
            except:
                username = user.username

            data = {
                "review" : review,
                "username" : username
            }

        review_items.append(data)

    context = {
        "products": products,
        "facebook": facebook,
        "instagram": instagram,
        "youtube": youtube,
        "tiktok": tiktok,
        "twitter": twitter,
        "telegram": telegram,
        "cat_fb": cat_fb,
        "cat_it": cat_it,
        "cat_yt": cat_yt,
        "cat_tt": cat_tt,
        "cat_tw": cat_tw,
        "cat_tg": cat_tg,
        "order": order,
        "items": items,
        "reviews": reviews,
        "review_items": review_items,
    }

    ctx2 ={"data": data, "products": products, "facebook": facebook, "instagram": instagram, "youtube": youtube, "tiktok": tiktok, "twitter": twitter}
    return render(request, "client/index.html",context)

def reviews(request):
    reviews = Review.objects.filter(status=True)

    data = cartData(request)
    order = data['order']

    review_items = []

    for review in reviews:
        user = review.user
        if user is None:
            username = "Anonymous"
            data = {
                "review" : review,
                "username" : username
            }
        else:
            try:
                app_user = AppUser.objects.get(user_id=user.id)
                username = app_user.fname + " " + app_user.lname
            except:
                username = user.username

            data = {
                "review" : review,
                "username" : username
            }

        review_items.append(data)
    return render(request, "client/reviews.html", {"review_items": review_items, "cat_fb": cat_fb,
        "cat_it": cat_it,
        "cat_yt": cat_yt,
        "cat_tt": cat_tt,
        "cat_tw": cat_tw,
        "cat_tg": cat_tg,
        "order": order,})

def terms(request):
    data = cartData(request)
    order = data['order']
    return render(request, "client/terms.html", {"cat_fb": cat_fb,
        "cat_it": cat_it,
        "cat_yt": cat_yt,
        "cat_tt": cat_tt,
        "cat_tw": cat_tw,
        "cat_tg": cat_tg,
        "order": order,})

def policy(request):
    data = cartData(request)
    order = data['order']
    return render(request, "client/policy.html", {"cat_fb": cat_fb,
        "cat_it": cat_it,
        "cat_yt": cat_yt,
        "cat_tt": cat_tt,
        "cat_tw": cat_tw,
        "cat_tg": cat_tg,
        "order": order,})

def allService(request):
    products = serviceProduct.objects.all().exclude(category__name="Marketing").exclude(category__name="Facebook Services").exclude(category__name="Instagram Services").exclude(category__name="Youtube Services").exclude(category__name="Tiktok Services").exclude(category__name="Twitter Services").exclude(category__name="Telegram Services")
    all_products = []
    all_prods = []
    active_products = products.filter(status=True)
    inactive_products = products.filter(status=False)
    data = cartData(request)
    order = data['order']
    for active in active_products:
        all_products.append(active)
        variable = variableProductPrice.objects.filter(product__id=active.id)
        try:
            price_filter = variable.values_list('price').annotate(Min('price')).order_by('price').first()
            product = {
                'product': active,
                'price': price_filter[1]
            }
            all_prods.append(product)
        except:
            product = {
                'product': active,
                'price': 00
            }
            all_prods.append(product)

    for inactive in inactive_products:
        all_products.append(inactive)
        variable = variableProductPrice.objects.filter(product__id=active.id)
        try:
            price_filter = variable.values_list('price').annotate(Min('price')).order_by('price').first()
            product = {
                'product': inactive,
                'price': price_filter[1]
            }
            all_prods.append(product)
        except:
            product = {
                'product': inactive,
                'price': 00
            }
            all_prods.append(product)

    return render(request, "client/allservices.html", {
                                        "all_products": all_prods,
                                        "products": all_products, "order": order, 
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def allSocial(request):
    marketing = serviceProduct.objects.filter(category__name="Marketing")
    facebook = serviceProduct.objects.filter(category__name="Facebook Services")
    instagram = serviceProduct.objects.filter(category__name="Instagram Services")
    youtube = serviceProduct.objects.filter(category__name="Youtube Services")
    tiktok = serviceProduct.objects.filter(category__name="Tiktok Services")
    twitter = serviceProduct.objects.filter(category__name="Twitter Services")
    telegram = serviceProduct.objects.filter(category__name="Telegram Services")

    cat_fb = productCategory.objects.get(name="Facebook Services").id
    cat_it = productCategory.objects.get(name="Instagram Services").id
    cat_yt = productCategory.objects.get(name="Youtube Services").id
    cat_tt = productCategory.objects.get(name="Tiktok Services").id
    cat_tw = productCategory.objects.get(name="Twitter Services").id
    cat_tg = productCategory.objects.get(name="Telegram Services").id

    data = cartData(request)
    order = data['order']

    context = {
        "facebook": facebook,
        "instagram": instagram,
        "youtube": youtube,
        "tiktok": tiktok,
        "twitter": twitter,
        "telegram": telegram,
        "cat_fb": cat_fb,
        "cat_it": cat_it,
        "cat_yt": cat_yt,
        "cat_tt": cat_tt,
        "cat_tw": cat_tw,
        "cat_tg": cat_tg,
        "order": order
    }

    return render(request, "client/allsocial.html", context)

def completeService(request):
    products = serviceProduct.objects.all()
    all_products = []
    all_prods = []
    active_products = products.filter(status=True)
    inactive_products = products.filter(status=False)
    data = cartData(request)
    order = data['order']
    for active in active_products:
        all_products.append(active)
        variable = variableProductPrice.objects.filter(product__id=active.id)
        try:
            product = {
                'product': active,
                'price': variable.first().price
            }
            all_prods.append(product)
        except:
            product = {
                'product': active,
                'price': 00
            }
            all_prods.append(product)

    for inactive in inactive_products:
        all_products.append(inactive)
        variable = variableProductPrice.objects.filter(product__id=active.id)
        try:
            product = {
                'product': inactive,
                'price': variable.first().price
            }
            all_prods.append(product)
        except:
            product = {
                'product': inactive,
                'price': 00
            }
            all_prods.append(product)

    return render(request, "client/completeservices.html", {
                                        "all_products": all_prods,
                                        "products": all_products, "order": order, 
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def contactUs(request):
    data = cartData(request)
    order = data['order']
    return render(request, "client/contact-us.html", {"order": order, 
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def saveRequest(request):
    post_data = request.POST

    ticket = Ticket(
        fname=post_data['fname'],
        lname=post_data['lname'],
        telid=post_data['telid'],
        subject=post_data['subject'],
        social=post_data['social'],
        budget=post_data['budget'],
        message=post_data['message']
    )

    ticket.save()
    return redirect('requestconfirm')

def requestConfirm(request):
    return render(request, "client/contact-done.html")

def listTickets(request):
    tickets = Ticket.objects.all()
    tcount = tickets.filter(seen=False).count()
    return render(request, "clientdash/ticketlist.html", {"tickets": tickets, "tcount": tcount, "scount": scount})

def ticketDetail(request, tid):
    ticket = Ticket.objects.get(id=tid)
    tcount = Ticket.objects.filter(seen=False).count()
    return render(request, "clientdash/ticketdetail.html", {"ticket": ticket, "tcount": tcount, "scount": scount})

def ticketSeen(request, tid):
    ticket = Ticket.objects.get(id=tid)
    ticket.seen = True
    ticket.save()
    return redirect('ticketdetail', tid)

def socialServices(request, cid):
    cat = productCategory.objects.get(id=cid)
    products = serviceProduct.objects.filter(category__id=cid)
    items = []
    for prod in products:
        variable = variableProductPrice.objects.filter(product__id=prod.id)
        try:
            price_filter = variable.values_list('price').annotate(Min('price')).order_by('price').first()
            product = {
                'product': prod,
                'price': price_filter[1]
            }
            items.append(product)
        except:   
            product = {
                'product': prod,
                'price': 00
            }
            items.append(product)

    return render(request, "client/index-category.html", {
                                        "items": items, "products": products, "cat": cat,
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,
                                         })

def clientServiceDetail(request, pid):
    data = ""
    review_items = []
    checkout = False
    product = serviceProduct.objects.get(id=pid)
    variables = variableProductPrice.objects.filter(product_id=pid).order_by('measurement')
    terms = productTerms.objects.filter(product_id=pid)
    reviews = Review.objects.filter(product_id=pid).filter(status=True)
    data = cartData(request)
    order = data['order']
    items = data['items']

    for review in reviews:
        user = review.user
        if user is None:
            username = "Anonymous"
            data = {
                "review" : review,
                "username" : username
            }
        else:
            try:
                app_user = AppUser.objects.get(user_id=user.id)
                username = app_user.fname + " " + app_user.lname
            except:
                username = user.username

            data = {
                "review" : review,
                "username" : username
            }

        review_items.append(data)


    for item in items:
        if item.product.id == pid:
            checkout = True

    print(review_items)

    return render(request, "client/detail.html", {"data": data, "product": product, "variables": variables, "order": order, "terms": terms, "reviews": reviews, "review_items": review_items,
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,
                                        "checkout": checkout})

def loadPrice(request):
    price_id = request.GET.get('price_id')
    product_id = request.GET.get('product_id')


    product = serviceProduct.objects.get(id=product_id)
    pricing = variableProductPrice.objects.get(id=price_id)

    base_price = product.base_price
    base_qty = product.base_qty

    if base_price == None or base_qty == None:
        base_price = 0
        base_qty = 0

    variable_price = pricing.price
    variable_qty = pricing.measurement

    if base_qty == 0:
        multiplier = 1
    else:
        multiplier = variable_qty / base_qty

    primary_price = base_price * multiplier

    if primary_price <= variable_price:
        data = {
            "base": None,
            "main": variable_price
        }
    else:
        data = {
            "base": primary_price,
            "main": variable_price
        }


    print(data)

    return render(request, 'client/loadprice.html', {"data": data})


def clientOrders(request):
    data = ""
    orders = Order.objects.filter(customer=request.user.username).filter(cancelled=False)
    cancelled_orders = Order.objects.filter(customer=request.user.username).filter(cancelled=True)
    data = cartData(request)
    order = data['order']
    return render(request, "client/orders.html", {"data": data, "orders": orders, "order": order,"cancelled_orders": cancelled_orders,
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def allOrders(request):
    data = ""
    return render(request, "orders.html", {"data": data})

def orderDetail(request, oid):
    data = ""
    order = Order.objects.get(id=oid)
    orderItems = OrderItems.objects.filter(order_id=oid)
    # order.get_cart_items = 0
    if order.payment.credit_type == "crypto":
        proofs = cryptoProof.objects.filter(order_id=oid)
        context = {'items': orderItems, 'order':order, 'proofs': proofs, "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,}
    else:
        context = {'items': orderItems, 'order':order , "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,}
    
    return render(request, "client/order_detail.html", context)

# CLIENT DASHBOARD

def createProduct(request):
    data = ""
    categories = productCategory.objects.filter(catstatus__status=True)
    return render(request, "clientdash/create_product.html", {"data": data, "categories": categories})

def saveProduct(request):
    data = ""
    post_data = request.POST
    file_data = request.FILES
    cat_id = post_data['category']
    category = productCategory.objects.get(id=cat_id)

    product = serviceProduct(
        name = post_data['name'],
        ptype = post_data['type'],
        category = category,
        description = post_data['description'],
        thumb = file_data['thumb_image']
    )

    product.save()
    return redirect('productlist')

def saveCategory(request):
    post_data = request.POST

    category = productCategory(
        name = post_data['name']
    )

    category.save()

    stat = catstatus(
        cat = category,
        status = True
    )
    stat.save()

    return redirect('createproduct')

def categoryList(request):
    categorys = productCategory.objects.all()

    return render(request, "clientdash/category_list.html", {"categorys": categorys})

def activateCategory(request, cid):
    cat = productCategory.objects.get(id=cid)

    try:
        cat.catstatus.status = True
        cat.catstatus.save()
    except:
        stat = catstatus(
            cat = cat,
            status = True
        )
        stat.save()

    return redirect('categorylist')

def deactivateCategory(request, cid):
    cat = productCategory.objects.get(id=cid)
    cat.catstatus.status = False
    cat.catstatus.save()
    return redirect('categorylist')

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
    terms = productTerms.objects.filter(product_id=pid)
    reviews = Review.objects.filter(product_id=pid)
    print(reviews)
    return render(request, "clientdash/product_detail.html", {"product": product, "inactive": inactive, "active": active, "variables": variables, "terms": terms, "reviews": reviews})

def updateDetail(request):
    post_data = request.POST
    product = serviceProduct.objects.get(id=post_data['pid'])

    product.description = post_data['description']
    product.save()

    return redirect('productdetail', post_data['pid'])

def saveVariablePrice(request):
    data = ""
    post_data = request.POST
    product = serviceProduct.objects.get(id=post_data['pid'])
    variable = variableProductPrice(
        product=product,
        measurement=post_data['measurement'],
        title=post_data['title'],
        price=post_data['price']
    )
    variable.save()
    return redirect('productdetail', post_data['pid'])

def saveTerms(request):
    post_data = request.POST
    product = serviceProduct.objects.get(id=post_data['pid'])
    terms = productTerms(
        product = product,
        terms = post_data['terms']
    )

    terms.save()
    return redirect('productdetail', post_data['pid'])

def saveBasePrice(request):
    data = ""
    post_data = request.POST

    product = serviceProduct.objects.get(id=post_data['pid'])
    product.base_price = post_data['base_price']
    product.base_qty = post_data['base_qty']

    product.save()

    return redirect('productdetail', post_data['pid'])

def updateVariablePrice(request, vid):
    variable = variableProductPrice.objects.get(id=vid)
    return render(request, "clientdash/update_variable_price.html", {"variable": variable})

def saveUpdatedVariablePrice(request):
    post_data = request.POST
    variable = variableProductPrice.objects.get(id=post_data['vid'])
    variable.price = post_data['price']
    variable.measurement = post_data['measurement']

    variable.save()

    return redirect('productdetail', variable.product.id)

def reviewList(request):
    reviews = Review.objects.all()
    return render(request, "clientdash/review_list.html", {"reviews": reviews})

def reviewAccept(request, rid):
    review = Review.objects.get(id=rid)
    pid = review.product.id
    review.status = True
    review.save()

    return redirect('productdetail', pid)

def reviewDecline(request, rid):
    review = Review.objects.get(id=rid)
    pid = review.product.id
    review.delete()

    return redirect('productdetail', pid)

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
    users = AppUser.objects.all()
    return render(request, "clientdash/client_list.html", {"data": data, "users": users})

def clientDetail(request, cid):
    client = AppUser.objects.get(id=cid)
    return render(request, "clientdash/client_detail.html", {"client": client})


def orderList(request):
    data = ""
    orders = Order.objects.all()
    crypto_orders = orders.filter(payment__credit_type="crypto")
    stripe_orders = orders.filter(payment__credit_type="stripe")
    print(crypto_orders)
    print(stripe_orders)
    return render(request, "clientdash/order_list.html", 
                {"data": data, "orders": orders, "stripe_orders": stripe_orders, "crypto_orders": crypto_orders})

def orderDetailDash(request, oid):
    data = ""
    order = Order.objects.get(id=oid)
    order.new_order = False
    order.save()
    orderItems = OrderItems.objects.filter(order_id=oid)
    if order.payment.credit_type == "crypto":
        
        proofs = cryptoProof.objects.filter(order_id=oid)
        print(proofs)
        context = {'items': orderItems, 'order':order, 'proofs': proofs}
    else:
        context = {'items': orderItems, 'order':order}
    
    return render(request, "clientdash/order_detail.html", context)


def submitReview(request, pid):
    product = serviceProduct.objects.get(id=pid)

    post_data = request.POST
    if request.user.is_authenticated:

        review = Review(
            product=product,
            review=post_data['review'],
            user=request.user,
        )

        review.save()
    else:
        review = Review(
            product=product,
            review=post_data['review']
        )
        review.save()

    return redirect('clientservicedetail', pid)


def updateItem(request):
    print("inside Update Item")
    data = json.loads(request.body)
    print(data)
    # {'productId': '1', 'action': 'add', 'price': '2'}
    productId = data['productId']
    action = data['action']
    price = data['price']
    link = data['link']
    reference = data['reference']
    print(link)
    print(productId)

    if request.user.is_authenticated:
        customer = request.user.username
    else:
        n = random.random()
        # customer = "Anonymous" + str(n)
        if not request.session.session_key:
            request.session.save()

        session = request.session.session_key
        print(session)
        customer = session
    product = serviceProduct.objects.get(id=productId)
    variance  = variableProductPrice.objects.get(id=price)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItems.objects.get_or_create(order=order, product=product, variance=variance, link=link, reference=reference)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        # orderItem.quantity = (orderItem.quantity - 1)
        orderItem.delete()

    orderItem.save()

    print(orderItem)

    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item Was Added', safe=False)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order':order, 'cartItems': cartItems, "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,}
    return render(request, "client/cart.html", context)

def removeCartItem(request, iid):
    orderitem = OrderItems.objects.get(id=iid)
    orderitem.delete()

    return redirect('cart')

def checkout(request, oid):
    data = ""
    params = {
        "access_key": "e9bca0873fefe06bb0145b67feb8ec24"
        }
    response = requests.get('http://api.coinlayer.com/live', params=params)
    
    crypto_data = response.json()
    # rates = crypto_data['rates']

    try:
        billing = Billing.objects.get(order_id=oid)
    except:
        billing = False
    
    order = Order.objects.get(id=oid)
    order_items = OrderItems.objects.filter(order_id=oid)

    auth_status = False

    if request.user.is_authenticated:
        auth_status = True
        
    return render(request, "client/checkout.html", {"data": data, 'order': order, 'order_items': order_items, "auth_status": auth_status, "billing": billing,
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})


# <QueryDict: {'csrfmiddlewaretoken': ['Ka4Nh9QauQ361lj7sH5F09KVFkGptdqV8IUl8IgoDvbUOBvM5Yi25xqXx7tM0xwz'], 
# 'order': ['2'], 'firstname': ['Hasan'], 'lastname': ['Mahmud'], 'username': ['hmahmud01'], 'email': ['hmahmud01@example.com'], 
# 'address': ['Shantinagar'], 'address2': [''], 'country': ['Bangladesh'], 'state': ['Dhaka'], 'zipcode': ['1217'], 
# 'credit_type': ['on'], 'currency': ['{"AMB" : "0.009838"}']}>

def processOrder(request):
    if request.user.is_authenticated:
        data = ""
        post_data = request.POST
        order = Order.objects.get(id=post_data['order'])
        
        try:
            billing = Billing.objects.get(order_id=order.id)
        except:
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

        try:
            payment = Payment.objects.get(order_id=order.id)
        except:
            payment = Payment(
                order = order,
                credit_type = post_data['credit_type'],
                total = order.get_cart_total
            )

            payment.save()

        if post_data['credit_type'] == "crypto":
            order.complete = False
            order.trx_id = "ORDER - " + str(order.id)
            timedate = datetime.datetime.now()
            updated_timedate = datetime.timedelta(hours=HOURS_DELTA)
            updated_time = timedate + updated_timedate

            today_updated = updated_time.date()

            today_date = today_updated.strftime("%m/%d/%Y")
            order.date_ordered = today_updated
            order.save()
            return redirect('cryptocheckout', order.id)
        else:
            return redirect('stripecheckout', order.id)
    
    else:
        post_data = request.POST

        if post_data['pass'] == post_data['conf_pass']:

            try:
                user = User.objects.create_user(post_data['email'], post_data['email'], post_data['pass'])
            except:
                data = ""
                params = {
                    "access_key": "e9bca0873fefe06bb0145b67feb8ec24"
                    }
                response = requests.get('http://api.coinlayer.com/live', params=params)
                
                crypto_data = response.json()
                rates = crypto_data['rates']
                
                order = Order.objects.get(id=post_data['order'])
                order_items = OrderItems.objects.filter(order_id=post_data['order'])

                auth_status = False

                if request.user.is_authenticated:
                    auth_status = True
                
                msg = f"User Already exists with this email {post_data['email']}"

                return render(request, "client/checkout.html", {"data": data, "rates": rates, 'order': order, 'order_items': order_items, "auth_status": auth_status, "msg": msg, "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

            appuser = AppUser(
                user = user,
                fname = post_data['firstname'],
                lname = post_data['lastname'],
                telid = post_data['username'],
                email = post_data['email'],
                address = post_data['address'],
                country = post_data['country'],
                state = post_data['state'],
                zipcode = post_data['zipcode']
            )

            appuser.save()

            order = Order.objects.get(id=post_data['order'])

            order.customer = user.username
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
                total = order.get_cart_total
            )

            payment.save()

            auth_login(request, user)

            if post_data['credit_type'] == "crypto":
                order.complete = True
                order.trx_id = "ORDER - " + str(order.id)
                timedate = datetime.datetime.now()
                updated_timedate = datetime.timedelta(hours=HOURS_DELTA)
                updated_time = timedate + updated_timedate

                today_updated = updated_time.date()

                today_date = today_updated.strftime("%m/%d/%Y")
                order.date_ordered = today_updated
                order.save()
                return redirect('cryptocheckout', order.id)
            else:
                return redirect('stripecheckout', order.id)

        else:
            data = ""
            params = {
                "access_key": "e9bca0873fefe06bb0145b67feb8ec24"
                }
            response = requests.get('http://api.coinlayer.com/live', params=params)
            
            crypto_data = response.json()
            rates = crypto_data['rates']
            
            order = Order.objects.get(id=post_data['order'])
            order_items = OrderItems.objects.filter(order_id=post_data['order'])

            auth_status = False

            if request.user.is_authenticated:
                auth_status = True
            
            msg = "Password Didn't Match"

            return render(request, "client/checkout.html", {"data": data, "rates": rates, 'order': order, 'order_items': order_items, "auth_status": auth_status, "msg": msg, "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})
      

def confirmCryptoOrder(request, oid):
    order = Order.objects.get(id=oid)
    billing = Billing.objects.get(order__id=oid)

    order.order_payment = True
    timedate = datetime.datetime.now()
    updated_timedate = datetime.timedelta(hours=HOURS_DELTA)
    updated_time = timedate + updated_timedate

    today_updated = updated_time.date()

    today_date = today_updated.strftime("%m/%d/%Y")
    order.date_ordered = today_updated
    order.save()

    return redirect('orderlistdetail', oid)

def cancelOrder(request, oid):
    order = Order.objects.get(id=oid)
    order.cancelled = True
    # order.delete()
    order.save()
    return redirect('orderlist')

def stripeCheckout(request, oid):
    return render(request, "client/checkout-stripe.html", {"oid": oid, "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def cryptoCheckout(request, oid):
    order = Order.objects.get(id=oid)
    return render(request, "client/checkout-crypto.html", {
                                        "order": order,
                                        "oid": oid,
                                        "cat_fb": cat_fb,   
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def saveCryptoProof(request, oid):
    
    post_data = request.POST
    file_data = request.FILES
    print(post_data)
    print(file_data)

    if post_data['hash'] != '' or file_data.getlist('proof_img') != [] :
        order = Order.objects.get(id=oid)

        networks = cryptoNetwork(
            order=order,
            network=post_data['network'],
            payment_hash=post_data['hash']
        )
        networks.save()

        order.complete = True
        order.order_payment = False
        order.save()

        if file_data:
            images = file_data.getlist('proof_img')

            for image in images:
                proofs = cryptoProof(
                    order=order,
                    proof=image
                )
                proofs.save()

        return redirect('cryptosuccess', oid)
    else:
        msg = "You didn't enter any payment proof or proof hash for the successful payment."
        return render(request, "client/checkout-crypto.html", {
                                        "oid": oid,
                                        "msg": msg,
                                        "cat_fb": cat_fb,   
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

    

def cryptoSuccess(request, oid):
    order = Order.objects.get(id=oid)
    orderItems = OrderItems.objects.filter(order_id=order.id)
    return render(request, "client/checkout-crypto-proof.html", {
                                        "order": order,
                                        "items": orderItems,
                                        "cat_fb": cat_fb,   
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def create_checkout_session(request, oid):
    order = Order.objects.get(id=oid)
    order_name = "ORD - " + str(order.id)
    amount = order.get_cart_total * 100
    # YOUR_DOMAIN = "http://127.0.0.1:8000"
    # YOUR_DOMAIN = "http://174.138.27.160:8000"
    YOUR_DOMAIN = "http://cryptomarketers.net/"
    product = stripe.Product.create(name=order_name)

    price = stripe.Price.create(
        unit_amount=int(amount),
        currency="usd",
        product=product.id,
    )
    checkout_session = stripe.checkout.Session.create(
        payment_method_types = ['card'],    
        line_items=[
            {
                'price': price.id,
                'quantity': 1,
            }
        ],
        mode="payment",
        success_url=YOUR_DOMAIN + '/checkout-success/',
        cancel_url=YOUR_DOMAIN + '/checkout-cancel/'
    )

    request.session['oid'] = oid
    request.session['cid'] = checkout_session.payment_intent

    return redirect(checkout_session.url, code=303)

def success(request):
    order = Order.objects.get(id=request.session['oid'])
    orderItems = OrderItems.objects.filter(order_id=order.id)
    checkout_id = request.session['cid']
    billing = Billing.objects.get(order__id=order.id)
    order.complete = True
    order.trx_id = checkout_id
    order.order_payment = True
    timedate = datetime.datetime.now()
    updated_timedate = datetime.timedelta(hours=HOURS_DELTA)
    updated_time = timedate + updated_timedate

    today_updated = updated_time.date()

    today_date = today_updated.strftime("%m/%d/%Y")
    order.date_ordered = today_updated
    order.save()

    try:
        del request.session['oid']
        del request.session['cid']
    except:
        pass

    # subject = 'Order Completion'
    # message = f'Hi {order.customer},\nYour Order has been placed in our system. Your order number is {order.id}.\nPlease Visit your orders page to see the detail of your order.\nThanks\n-Absolute Point.'
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [billing.email, ]
    # send_mail( subject, message, email_from, recipient_list )

    return render(request, 'client/success.html', {
                                        "items": orderItems,
                                        "order": order,
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def cancel(request):
    return  render(request, 'client/cancel.html', {
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

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
    data = cartData(request)
    order = data['order']
    return render(request, "client/portfolio.html", {"portfolios": portfolios, "order": order,
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def portfolioDetail(request, pid):
    portfolio = Portfolio.objects.get(id=pid)
    contributors = PortfolioContributors.objects.filter(portfolio_id=pid)
    proofs = PortfolioProves.objects.filter(portfolio_id=pid)
    data = cartData(request)
    order = data['order']
    return render(request, "client/portfolio_detail.html", {"portfolio": portfolio, "contributors": contributors, 'proofs': proofs, "order": order,
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def people(request):
    people = DashboardUser.objects.all()

    return render(request, "client/people.html", {"people": people})

def peopleDetail(request, pid):
    dashuser = DashboardUser.objects.get(id=pid)
    portfolios = PortfolioContributors.objects.filter(contributor_id=pid)

    return render(request, "client/people_detail.html", {"dashuser": dashuser, "portfolios": portfolios})

def createNews(request):
    return render(request, "clientdash/create_news.html")

def saveNews(request):
    post_data = request.POST
    file_data = request.FILES
    news = News(
        title = post_data['title'],
        message = post_data['message'],
        msg_2 = post_data['msg_2'],
        thumb = file_data['thumb']
    )

    news.save()
    return redirect('listnews')

def listNews(request):
    news = News.objects.all()
    return render(request, "clientdash/news_list.html", {"news": news})

def newsDelete(request, nid):
    news = News.objects.get(id=nid)
    news.delete()
    return redirect('listnews')

def detailNews(request, nid):
    news = News.objects.get(id=nid)
    return render(request, "clientdash/news_detail.html", {"news": news})


def newsList(request):
    news = News.objects.all()
    return render(request, "client/newslist.html", {"news": news, 
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def newsDetail(request, nid):
    news = News.objects.get(id=nid)
    return render(request, "client/newsdetail.html", {"news": news, 
                                        "cat_fb": cat_fb,
                                        "cat_it": cat_it,           
                                        "cat_yt": cat_yt,
                                        "cat_tt": cat_tt,
                                        "cat_tw": cat_tw,
                                        "cat_tg": cat_tg,})

def removeData(request):
    productCategory.objects.all().delete()
    catstatus.objects.all().delete()
    serviceProduct.objects.all().delete()
    variableProductPrice.objects.all().delete()
    productTerms.objects.all().delete()
    Order.objects.all().delete()
    cryptoNetwork.objects.all().delete()
    cryptoProof.objects.all().delete()
    OrderItems.objects.all().delete()
    Billing.objects.all().delete()
    Payment.objects.all().delete()
    Review.objects.all().delete()

    return redirect('home')
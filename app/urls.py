from os import name
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from app import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('verifylogin/', views.verifyLogin, name="verifylogin"),
    path('logout/', views.userLogout, name="logout"),
    path('register/', views.register, name="register"),
    path('adduser/', views.addUser, name="adduser"),
    path('resetpassword/', views.resetPassword, name="resetpassword"),
    path('changepassword/', views.changePassword, name="changepassword"),
    path('registeruser/', views.registerUser, name="registeruser"),
    path('updateuser/', views.updateUser, name="updateuser"),
    path('detailuser/<int:uid>/', views.detailUser, name="detailuser"),
    path('reupdateuser/', views.reupdateUser, name="reupdateuser"),
    path('', views.home, name="home"),    
    path('salesdashboard/', views.salesDashboard, name="salesdashboard"),
    path('searchresult', views.searchResult, name="searchresult"),
    path('noticecreate/', views.noticeCreate, name="noticecreate"),
    path('savenotice/', views.saveNotice, name="savenotice"),
    path('noticedetail/<int:nid>/', views.noticeDetail, name="noticedetail"),
    path('servicecreate/', views.serviceCreate, name="servicecreate"),
    path('serviceupdate/<int:sid>/', views.serviceUpdate, name="serviceupdate"),
    path('udpateservicevalue/<int:sid>/', views.updateServiceValue, name="udpateservicevalue"),
    path('saveservice/', views.saveService, name="saveservice"),
    path('addservice/', views.addService, name="addservice"),
    path('addservicelist/', views.addServiceList, name="addservicelist"),
    path('removeservicelist/<int:sid>/', views.removeServiceList, name="removeservicelist"),
    path('updateservicelist/', views.updateServiceList, name="updateservicelist"),
    path('addservicetype/', views.addServiceType, name="addservicetype"),
    path('addservicetypelist/', views.addServiceTypeList, name="addservicetypelist"),
    path('removeservicetypelist/<int:sid>/', views.removeServiceTypeList, name="removeservicetypelist"),
    path('servicedetail/<int:sid>/', views.serviceDetail, name="servicedetail"),
    path('acceptservice/<int:sid>/', views.acceptService, name="acceptservice"),
    path('declineservice/<int:sid>/', views.declineService, name="declineservice"),
    path('addservicepayment/', views.addServicePyament, name="addservicepayment"),
    path('acceptpayment/<int:pid>/', views.acceptPayment, name="acceptpayment"),
    path('declinepayment/<int:pid>/', views.declinePayment, name="declinepayment"),
    path('donepayment/<int:sid>/', views.donePayment, name="donepayment"),
    path('fraudpayment/<int:sid>/', views.fraudPayment, name="fraudpayment"),
    path('otherpayment/<int:sid>/', views.otherPayment, name="otherpayment"),
    path('servicelist/', views.serviceList, name="servicelist"),
    path('servicetypelist/', views.serviceTypeList, name="servicetypelist"),
    path('salesservices/', views.salesServices, name="salesservices"),
    path('accounts/', views.accountsIndex, name="accounts"),
    path('accountsdetail/<int:aid>/', views.accountsDetail, name="accountsdetail"),    
    path('monthlysales/', views.monthlySales, name='monthlysales'),
    path('monthlysales/detail/<int:mm>/<int:yy>', views.monthlySaleDetail, name='monthlysalesdetail'),
    path('client/index/', views.clientIndex, name="clientindex"),
    path('client/service/detail', views.clientServiceDetail, name="clientservicedetail"),
    path('client/orders', views.clientOrders, name="clientorders"),
    path('client/order/detail', views.orderDetail, name="orderdetail"),
    path('allorders/', views.allOrders, name="allorders"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
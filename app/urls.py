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
    path('', views.home, name="home"),    
    path('salesdashboard/', views.salesDashboard, name="salesdashboard"),
    path('noticecreate/', views.noticeCreate, name="noticecreate"),
    path('savenotice/', views.saveNotice, name="savenotice"),
    path('noticedetail/<int:nid>/', views.noticeDetail, name="noticedetail"),
    path('servicecreate/', views.serviceCreate, name="servicecreate"),
    path('saveservice/', views.saveService, name="saveservice"),
    path('addservice/', views.addService, name="addservice"),
    path('addservicelist/', views.addServiceList, name="addservicelist"),
    path('updateservicelist/', views.updateServiceList, name="updateservicelist"),
    path('addservicetype/', views.addServiceType, name="addservicetype"),
    path('addservicetypelist/', views.addServiceTypeList, name="addservicetypelist"),
    path('servicedetail/<int:sid>/', views.serviceDetail, name="servicedetail"),
    path('acceptservice/<int:sid>/', views.acceptService, name="acceptservice"),
    path('addservicepayment/', views.addServicePyament, name="addservicepayment"),
    path('acceptpayment/<int:pid>/', views.acceptPayment, name="acceptpayment"),
    path('donepayment/<int:sid>/', views.donePayment, name="donepayment"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
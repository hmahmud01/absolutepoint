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
    path('dashboard/', views.home, name="home"),    
    path('salesdashboard/', views.salesDashboard, name="salesdashboard"),
    path('searchresult', views.searchResult, name="searchresult"),
    path('noticecreate/', views.noticeCreate, name="noticecreate"),
    path('savenotice/', views.saveNotice, name="savenotice"),
    path('noticedetail/<int:nid>/', views.noticeDetail, name="noticedetail"),
    path('duplicateservice/', views.duplicateService, name="duplicateservice"),
    path('servicecreate/', views.serviceCreate, name="servicecreate"),
    path('serviceupdate/<int:sid>/', views.serviceUpdate, name="serviceupdate"),
    path('udpateservicevalue/<int:sid>/', views.updateServiceValue, name="udpateservicevalue"),
    path('saveservice/', views.saveService, name="saveservice"),
    path('addservice/', views.addService, name="addservice"),
    path('addservicelist/', views.addServiceList, name="addservicelist"),
    path('removeservicelist/<int:sid>/', views.removeServiceList, name="removeservicelist"),
    path('updateservicelist/', views.updateServiceList, name="updateservicelist"),
    path('updateservicetype/', views.updateServiceType, name="updateservicetype"),
    path('removeuser/', views.removeUser, name="removeuser"),
    path('updateservicebonus/', views.updateServiceBonus, name="updateservicebonus"),
    path('servicebonus/<int:sid>/', views.serviceBonus, name ="servicebonus"),
    path('removeservicebonus/<int:sid>/', views.removeServiceBonus, name="removeservicebonus"),
    path('seasonbonus/', views.seasonBonus, name="seasonbonus"),
    path('addseasonbonus/', views.addSeasonBonus, name="addseasonbonus"),
    path('removeseasonbonus/<int:bid>/', views.removeSeasonBonus, name="removeseasonbonus"),
    path('submitseasonbons/', views.submitseasonbonus, name="submitseasonbonus"),
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
    path('salesexecutivesalary/', views.salesExecutiveSalary, name="salesexecutivesalary"),

    # CLIENT AREA
    path('', views.clientIndex, name="clientindex"),
    path('allservices/', views.allService, name="allservices"),
    path('allsocial', views.allSocial, name="allsocial"),
    path('completeservices/', views.completeService, name="completeservices"),
    path('socialservices/<int:cid>', views.socialServices, name="socialservices"),
    path('client/service/detail/<int:pid>/', views.clientServiceDetail, name="clientservicedetail"),
    path('ajax/load-price/', views.loadPrice, name="loadprice"),
    path('client/orders', views.clientOrders, name="clientorders"),
    path('client/order/detail/<int:oid>/', views.orderDetail, name="orderdetail"),
    path('allorders/', views.allOrders, name="allorders"),
    path('createproduct/', views.createProduct, name="createproduct"),
    path('saveproduct/', views.saveProduct, name="saveproduct"),
    path('productact/<int:pid>/<str:act>/', views.productAct, name ="productact"),
    path('savecat/', views.saveCategory, name="savecat"),
    path('productlist/', views.productList, name="productlist"),
    path('categorylist/', views.categoryList, name="categorylist"),
    path('activatecategory/<int:cid>/', views.activateCategory, name="activatecategory"),
    path('deactivatecategory/<int:cid>/', views.deactivateCategory, name="deactivatecategory"),
    path('productdetail/<int:pid>/', views.productDetail, name="productdetail"),
    path('updatedetail/', views.updateDetail, name="updatedetail"),
    path('savevariableprice/', views.saveVariablePrice, name="savevariableprice"),
    path('saveterms/', views.saveTerms, name="saveterms"),
    path('savebaseprice/', views.saveBasePrice, name="savebaseprice"),
    path('updatevariableprice/<int:vid>/', views.updateVariablePrice, name="updatevariableprice"),
    path('saveupdatedvariableprice/', views.saveUpdatedVariablePrice, name="saveupdatedvariableprice"),
    path('reviews/', views.reviewList, name="reviews"),
    path('reviewaccept/<int:rid>/', views.reviewAccept, name="reviewaccept"),
    path('reviewdecline/<int:rid>/',views.reviewDecline, name="reviewdecline"),
    path('orderlist/', views.orderList, name="orderlist"),
    path('orderlist/detail/<int:oid>/', views.orderDetailDash, name="orderlistdetail"),
    path('confirmcryptoorder/<int:oid>/', views.confirmCryptoOrder, name="confirmcryptoorder"),
    path('cancelorder/<int:oid>/', views.cancelOrder, name="cancelorder"),
    path('clientlist/', views.clientList, name="clientlist"),
    path('cart/', views.cart, name="cart"),
    path('removecartitem/<int:iid>/', views.removeCartItem, name="removecartitem"),
    path('submitreview/<int:pid>/', views.submitReview, name="submitreview"),
    path('update_item/', views.updateItem, name="update_item"),
    path('checkout/<int:oid>', views.checkout, name="checkout"), 
    path('stripecheckout/<int:oid>', views.stripeCheckout, name="stripecheckout"),
    path('savecryptoproof/<int:oid>', views.saveCryptoProof, name="savecryptoproof"),
    path('cryptocheckout/<int:oid>', views.cryptoCheckout, name="cryptocheckout"),
    path('cryptosuccess/<int:oid>/', views.cryptoSuccess, name="cryptosuccess"),
    path('checkout-success/', views.success, name='success'),
    path('checkout-cancel/', views.cancel, name='cancel'),
    path('create-checkout-session/<int:oid>', views.create_checkout_session, name="create-checkout-session"),
    path('processorder/', views.processOrder, name="processorder"),
    path('createportfolio/', views.createPortfolio, name="createportfolio"),
    path('saveportfolio/', views.savePortfolio, name="saveportfolio"),
    path('portfolio/', views.portfolio, name="portfolio"),
    path('portfoliodetail/<int:pid>/', views.portfolioDetail, name="portfoliodetail"),
    path('people/', views.people, name="people"),
    path('peopledetail/<int:pid>', views.peopleDetail, name="peopledetail"),
    path('contactus/', views.contactUs, name="contactus"),
    path('saverequest/', views.saveRequest, name="saverequest"),
    path('requestconfirm/', views.requestConfirm, name="requestconfirm"),
    path('ticketlist/', views.listTickets, name="ticketlist"),
    path('ticketdetail/<int:tid>', views.ticketDetail, name="ticketdetail"),
    path('ticketseen/<int:tid>', views.ticketSeen, name="ticketseen"),
    path('createnews/', views.createNews, name="createnews"),
    path('savenews/', views.saveNews, name="savenews"),
    path('listnews/', views.listNews, name="listnews"),
    path('detailnews/<int:nid>', views.detailNews, name="detailnews"),
    path('newslist/', views.newsList, name="newslist"),
    path('newsdetail/<int:nid>', views.newsDetail, name="newsdetail"), 

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
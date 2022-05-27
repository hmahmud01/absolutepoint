from os import stat
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BinaryField

class DashboardUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=64, default='sales', blank=True, null=True)
    username = models.CharField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    email = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    status = models.BooleanField(default=True)
    password_change = models.BooleanField(default=False)
    telegram_id = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class UserRank(models.Model):
    user = models.ForeignKey(DashboardUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=True, blank=True)
    tier = models.PositiveIntegerField(null=True, blank=True)
    sale_percent = models.FloatField(null=True, blank=True)
    current_earn = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name}-{self.title}"

class Service(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    comm_status = models.BooleanField(default=False)
    cap = models.FloatField(null=True, blank=True)
    commission = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title

class ServiceType(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    
    def __str__(self):
        return self.title

class Services(models.Model):
    user = models.ForeignKey(DashboardUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=64, null=True, blank=True)
    site_url = models.CharField(max_length=512, null=True, blank=True)
    counter = models.PositiveIntegerField(null=True, blank=True)
    ratio = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=128, null=True, blank=True)    
    accepted = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=128, null=True, blank=True)
    comm_status = models.BooleanField(default=False)
    commission = models.FloatField(null=True, blank=True)
    comm_amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}-{self.date}-{self.user.username} - {self.price}"
        # return str(self.title)

    def dateStamp(self):
        dd = self.created_at.strftime('%d')
        mm = self.created_at.strftime('%B')
        yy = self.created_at.strftime('%Y')
        date = yy
        return date

class SalesBonus(models.Model):
    emp = models.ForeignKey(DashboardUser, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    detail = models.CharField(max_length=512, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.emp.name} - {self.amount}"
    

class ServicePayments(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)            
    amount = models.FloatField(null=True, blank=True)
    link = models.CharField(max_length=512, null=True, blank=True)
    image = models.ImageField('payment_image', upload_to='payments', blank=True, null=True)
    accepted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.service.title}-{self.amount}"

class Notices(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    category = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    validity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


# CLIENT AREA MODELS

class productCategory(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

class serviceProduct(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    ptype = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(productCategory, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    thumb = models.ImageField('product_thumbs',upload_to='product_thumbs', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

class variableProductPrice(models.Model):
    product = models.ForeignKey(serviceProduct, on_delete=models.CASCADE)
    measurement = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.product.name

class Portfolio(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    thumb = models.ImageField('portfolio_thumbs',upload_to='portfolio_thums', null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, blank=True, null=True)

class PortfolioContributors(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    contributor = models.ForeignKey(DashboardUser, on_delete=models.CASCADE)

class PortfolioProves(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    image = models.ImageField('portfolio_proofs', upload_to='potfolio_proofs', null=True, blank=True)

class serviceOrder(models.Model):
    pass

class Client(models.Model):
    pass

class Order(models.Model):
    customer = models.CharField(max_length=128, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    trx_id = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitems_set.all()
        
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItems(models.Model):
    product = models.ForeignKey(serviceProduct, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    variance = models.ForeignKey(variableProductPrice, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def get_total(self):
        total = self.variance.price * self.quantity
        return total

class Billing(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=128, null=True, blank=True)
    lastname = models.CharField(max_length=128, null=True, blank=True)
    username = models.CharField(max_length=128, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    address2 = models.CharField(max_length=256, null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=64, null=True, blank=True)
    zipcode = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    credit_type = models.CharField(max_length=128, null=True, blank=True)
    currency_key = models.CharField(max_length=128, null=True, blank=True)
    currency_value =  models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return str(self.id)
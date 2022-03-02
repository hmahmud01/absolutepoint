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

    def __str__(self):
        return self.title

class ServiceType(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.title

class Services(models.Model):
    user = models.ForeignKey(DashboardUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=64, null=True, blank=True)
    site_url = models.CharField(max_length=512, null=True, blank=True)
    counter = models.PositiveIntegerField(null=True, blank=True)
    ratio = models.FloatField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=128, null=True, blank=True)    
    accepted = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}-{self.title}"
        # return str(self.title)

    def dateStamp(self):
        dd = self.created_at.strftime('%d')
        mm = self.created_at.strftime('%B')
        yy = self.created_at.strftime('%Y')
        date = yy
        return date

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
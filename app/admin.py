from django.contrib import admin

from .models import *

admin.site.register([DashboardUser, UserRank, Service, ServiceType, Services, ServicePayments, Notices])

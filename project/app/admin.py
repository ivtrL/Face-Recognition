from django.contrib import admin
from .models import Admin, User, Card, Device, Log, Time

admin.site.register([Admin, User, Card, Device, Log, Time])
from django.contrib import admin
from .models import UserInfo, UserRequests, ClearPrice, Cart, ClearHistory, Payment, ClearCount, Bot_logined

admin.site.register(UserInfo)
admin.site.register(UserRequests)
admin.site.register(ClearPrice)
admin.site.register(Cart)
admin.site.register(ClearHistory)
admin.site.register(Payment)
admin.site.register(ClearCount)
admin.site.register(Bot_logined)
# Register your models here.

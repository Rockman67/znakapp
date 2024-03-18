from django.conf import settings
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser



class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return '{0} '.format(self.user)


class UserRequests(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20)
    addres = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=now, editable=False)
    lot_link = models.TextField()
    download_link = models.TextField()

    def __str__(self):
        return '{0} '.format(self.user)


class ClearPrice(models.Model):
    clear_price = models.IntegerField()

    def __str__(self):
        return '{0} '.format(self.clear_price)


class User(AbstractUser):
    is_active = models.BooleanField(default=False)

    # Добавляем related_name, чтобы избежать конфликта с обратными ссылками по умолчанию
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='service_user_set',
        related_query_name='service_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='service_user_set',
        related_query_name='service_user',
    )


class Cart(models.Model):
    trial_quantity = models.PositiveIntegerField()
    trial_bonus = models.PositiveIntegerField()
    trial_access = models.CharField(max_length=10)
    trial_price_tn = models.DecimalField(max_digits=10, decimal_places=2)
    trial_price_eu = models.DecimalField(max_digits=10, decimal_places=2)
    

    beginer_quantity = models.PositiveIntegerField()
    beginer_bonus = models.PositiveIntegerField()
    beginer_access = models.CharField(max_length=10)
    beginer_price_tn = models.DecimalField(max_digits=10, decimal_places=2)
    beginer_price_eu = models.DecimalField(max_digits=10, decimal_places=2)

    advanced_quantity = models.PositiveIntegerField()
    advanced_bonus = models.PositiveIntegerField()
    advanced_access = models.CharField(max_length=10)
    advanced_price_tn = models.DecimalField(max_digits=10, decimal_places=2)
    advanced_price_eu = models.DecimalField(max_digits=10, decimal_places=2)

    expert_quantity = models.PositiveIntegerField()
    expert_bonus = models.PositiveIntegerField()
    expert_access = models.CharField(max_length=10)
    expert_price_tn = models.DecimalField(max_digits=10, decimal_places=2)
    expert_price_eu = models.DecimalField(max_digits=10, decimal_places=2)

# class CartItem(models.Model):
#     product = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

class ClearHistory(models.Model):
    user = models.CharField(max_length=100)
    platform = models.CharField(max_length=30)
    params = models.TextField()
    date = models.DateTimeField(default=now, editable=False)
    lot_link = models.TextField()
    
    def __str__(self):
        return f"ClearHistory ID: {self.id}"

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.TextField()
    amount = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Email : {self.email}"
    
    
class ClearCount(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.TextField()
    count = models.IntegerField(default=0)
    bonus_count = models.IntegerField(default=0)
    tarif = models.CharField(max_length=100,default="Пробный")
    def __str__(self):
        return f"Info : {self.email, self.count, self.tarif}"

    
class Bot_logined(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.TextField()
    status = models.BooleanField()
    nickname = models.TextField()
    def __str__(self):
        return f"Info : {self.email,self.status}"

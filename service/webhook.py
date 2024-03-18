#from celery import shared_task
# Файл обработки  нашего json файла, полученым во views спомощью webhook
import json
from .models import Payment,ClearCount
from django.db.models import F

def process_json_data(json_data):
    json_load = json.loads(json_data)
    our_email = json_load['customer_email']
    total_amount = json_load['total_amount']
    phone = json_load['customer_phone']

    item = Payment(email=f"{our_email}", amount=f"{total_amount}", phone=f"{phone}")
    item.save()
    last_record = Payment.objects.last()
    email_value = last_record.email
    money_value = last_record.amount# ключ для списка tarifs
    print(email_value)
    objects_with_condition = Payment.objects.filter(email=email_value).first()
    #список ключ-значение, где ключ  - сумма оплаты
    tarifs =  {
        1.09: [10,'Начинающий',0],
        2.97:[25,'Продвинутый',5],
        5.30:[50,"Эксперт",10],
    }
    check_email = objects_with_condition.email
    try:
        ClearCount.objects.filter(email=check_email).update(count=F('count') + tarifs[money_value][0],tarif=tarifs[money_value][1],bonus_count=F('bonus_count') + tarifs[money_value][2])
    except Exception:
        print("Возникла ошибка ",Exception)

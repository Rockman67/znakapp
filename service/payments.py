# Этот файл был создан для тестирования обработки json файла
import json
from .models import Payment
from pprint import pprint
with open('data.json', 'r') as f:
    json_data = f.read()

# Преобразование строки JSON в словарь Python
data = json.loads(json_data)

# Получение списка транзакций
transactions = data['data']['wallet_transactions']

# Получение электронных адресов и общих сумм из каждой транзакции
for transaction in transactions:
    our_email = transaction['sale_form']['email']
    total_amount = transaction['total_amount']
    item = Payment(email=f"{our_email}", amout=f"{total_amount}")
    item.save()
    print(f"Email: {our_email}, Total Amount: {total_amount}")
# Вход на сайт MeltonPay
'''login_url = "https://api.mel.store/api/mel-store/auth/login"
login_payload = json.dumps({
  "email": "forrealtor.kz@gmail.com",
  "password": "payrealtor23"
})
login_headers = {
  'Content-Type': 'application/json'
}
login_response = requests.request("POST", login_url, headers=login_headers, data=login_payload)
login_data = login_response.json()

# Проверка успешного входа и получение токена доступа
if 'access_token' in login_data:
    access_token = login_data['access_token']
    
    # Получение списка транзакций с использованием токена доступа
    transactions_url = "https://api.mel.store/api/mel-store/wallet/2362/transactions?filter[type]=payment&filter[status]=payment_completed"
    transactions_headers = {
        'Authorization': 'Bearer ' + access_token
    }
    transactions_response = requests.request("GET", transactions_url, headers=transactions_headers)
    transactions_data = transactions_response.json()
    pprint(transactions_data)
else:
    print("Ошибка входа:", login_data)'''
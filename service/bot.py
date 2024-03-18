import telebot # telebot
import zipfile
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States
import os, time
# States storage
from telebot import types
from django.contrib.auth.models import User
from .models import ClearCount,Bot_logined,Cart
from .tasks import bot_delete_task,bot_execute_lama,bot_get_active_tasks
from django.db.models import F
from celery import current_app

class MyStates:
    start = 1
    login = 2
    password = 3
    info = 4
    price = 5
    clear = 6
    stop = 7

class Bot:
    def __init__(self, token):
        self.user_states = {}  # словарь для отображения состояний пользователей
        self.bot = telebot.TeleBot(token)
        self.user_info = {'login':''}
        
        @self.bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
        def handle_back_to_main(call):
            username = call.from_user.username
            self.send_main_menu(call.message.chat.id,username)
            self.user_states[call.from_user.id] = MyStates.start
            
        @self.bot.callback_query_handler(func=lambda call: call.data == 'login')
        def handle_login_callback(call):
            self.send_login_message(call.message.chat.id)
            self.user_states[call.from_user.id] = MyStates.login

        @self.bot.callback_query_handler(func=lambda call: call.data == 'password')
        def handle_password_callback(call):
            self.send_password_message(call.message.chat.id)
            self.user_states[call.from_user.id] = MyStates.password
        
        
        @self.bot.callback_query_handler(func=lambda call: call.data == 'info')
        def handle_info_callback(call):
            username = call.from_user.username
            print(username)
            self.send_info(call.message.chat.id,username)
            self.user_states[call.from_user.id] = MyStates.info
            
        @self.bot.callback_query_handler(func=lambda call: call.data == 'price')
        def handle_price_callback(call):
            self.send_price(call.message.chat.id)
            self.user_states[call.from_user.id] = MyStates.price
        
        @self.bot.callback_query_handler(func=lambda call: call.data == 'clear')
        def handle_clear_callback(call):
            username = call.from_user.username
            self.send_clear(call.message.chat.id,username)
            self.user_states[call.from_user.id] = MyStates.clear
            
            
        @self.bot.message_handler(commands=['start'])
        def start_ex(message):
            self.send_main_menu(message.chat.id,message.from_user.username)
            self.user_states[message.from_user.id] = MyStates.start
            
        @self.bot.message_handler(commands=['stop'])
        def start_ex(message):
            self.update_status(message.chat.id,message.from_user.username)
            self.user_states[message.from_user.id] = MyStates.stop

        
        @self.bot.message_handler(func=lambda message: self.user_states.get(message.from_user.id) == MyStates.login)
        def login_get(message):
            username = message.text
            print(username)
            user_info = User.objects.filter(username=message.text).first()
            if user_info:
                username = user_info.email
                kb = types.InlineKeyboardMarkup()
                bt_1 = types.InlineKeyboardButton(text='Ввести пароль', callback_data='password')
                kb.add(bt_1)
                self.bot.send_message(message.chat.id, "Username : {}".format(username),reply_markup=kb)
                self.user_info['login'] = f'{username}'
            else:
                kb = types.InlineKeyboardMarkup()
                bt_1 = types.InlineKeyboardButton(text='Заново', callback_data='login')
                kb.add(bt_1)
                self.bot.send_message(message.chat.id,"⚠Не верное имя пользователя", reply_markup=kb)
        @self.bot.message_handler(func=lambda message: self.user_states.get(message.from_user.id) == MyStates.password)
        def password_get(message):
            tagname = message.from_user.username
            username = self.user_info['login']
            user_info = User.objects.filter(username=username).first()
            if user_info.check_password(message.text):
                check_nickname = Bot_logined.objects.filter(email=username).first()
                if check_nickname:
                    Bot_logined.objects.filter(email=username).update(nickname=tagname,status=1)
                else:
                    new_instance = Bot_logined(email=username,status=1,nickname=tagname)
                    new_instance.save()
                kb = types.InlineKeyboardMarkup()
                bt_1 = types.InlineKeyboardButton(text='В главное меню', callback_data='main_menu')
                kb.add(bt_1)
                self.bot.send_message(message.chat.id,"Вы успешно вошли в аккаунт🔓",reply_markup=kb)
            else:
                kb = types.InlineKeyboardMarkup()
                bt_1 = types.InlineKeyboardButton(text='Ввести данные заново:', callback_data='login')
                kb.add(bt_1)
                self.bot.send_message(message.chat.id,"⚠Не верные данные!",reply_markup=kb)
        #обработка ссылки полученной от пользователя
        @self.bot.message_handler(func=lambda message: self.user_states.get(message.from_user.id) == MyStates.clear)
        def get_link(message):
            username = message.from_user.username
            print(username)
            lama_num = bot_get_active_tasks()
            self.bot.send_message(message.chat.id,"Бот начал свою работу, дождитесь обработки ) ")
            result = bot_execute_lama.delay(lama_num, message.text)
            print(f"Lama {lama_num} started")
            id = result.id
            while True:
                task = current_app.AsyncResult(id)
                time.sleep(1)
                if task.status == "SUCCESS":
                    print(f"Thread {lama_num}: OK")
                    break
            self.bot.send_message(message.chat.id,"Формируем для вас архив с фото ) ")
            photo_folder_path = "D:/work/znakapp/znakapp/service/static/out/bots1"
            photo_files = os.listdir(photo_folder_path)
            # Change the name of the ZIP file as desired
            temp_zip_name = "images.zip"
            temp_zip_path = os.path.join(photo_folder_path, temp_zip_name)
            with zipfile.ZipFile(temp_zip_path, 'w') as zipf:
                for file in photo_files:
                    file_path = os.path.join(photo_folder_path, file)
                    zipf.write(file_path, arcname=file)
            get_user_id = Bot_logined.objects.filter(nickname=username).first()
            if get_user_id:
                our_user_id = get_user_id.email
                get_clear_count = ClearCount.objects.filter(email=our_user_id).first()
                if get_clear_count:
                    if get_clear_count.bonus_count!=0:
                        ClearCount.objects.filter(email=our_user_id).update(bonus_count=F('bonus_count') - 1)
                    else:
                        ClearCount.objects.filter(email=our_user_id).update(count=F('count') - 1)
            with open(temp_zip_path, 'rb') as zip_file:
                    self.bot.send_document(message.chat.id, document=zip_file)
            kb = types.InlineKeyboardMarkup()
            bt_1 = types.InlineKeyboardButton("👤Аккаунт",callback_data='info')
            bt_2 = types.InlineKeyboardButton("📋Тарифы",callback_data='price')
            bt_3 = types.InlineKeyboardButton("✅Очистка",callback_data='clear')
            kb.add(bt_1, bt_2, bt_3)
            self.bot.send_message(message.chat.id, "Что нибудь ещё? {}",reply_markup=kb)
            bot_delete_task(lama_num)
            
            
    def send_clear(self,chat_id,username):
        print(username)
        check_user_id = Bot_logined.objects.filter(nickname=username).first()
        if check_user_id:
            our_user_id = check_user_id.email
            get_clear_count = ClearCount.objects.filter(email=our_user_id).first()
            if get_clear_count:
                if (get_clear_count.count == 0 and get_clear_count.bonus_count == 0) :
                    kb = types.InlineKeyboardMarkup()
                    bt_1 = types.InlineKeyboardButton("👤Аккаунт",callback_data='info')
                    bt_2 = types.InlineKeyboardButton("📋Тарифы",callback_data='price')
                    bt_3 = types.InlineKeyboardButton("✅Очистка",callback_data='clear')
                    kb.add(bt_1, bt_2, bt_3)
                    self.bot.send_message(chat_id, "У вас закончились очистки! Перейдите в магазин",reply_markup=kb)
                else:
                    kb = types.InlineKeyboardMarkup()
                    bt_1 = types.InlineKeyboardButton(text='Назад:', callback_data='main_menu')
                    kb.add(bt_1)
                    self.bot.send_message(chat_id, "Введите ссылку",reply_markup=kb)
    def send_price(self,chat_id):
        price_info = Cart.objects.all().first()
        kb = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton(text='Назад', callback_data='main_menu')
        bt_2 = types.InlineKeyboardButton(text='Купить', url='http://127.0.0.1:8000/price-list/')
        kb.add(bt_1,bt_2)
        if price_info:
            self.bot.send_message(chat_id,f'''
Тариф: Пробный 
Кол-во очисток : {price_info.trial_quantity} (бонусных : {price_info.trial_bonus}), Цена : {int(price_info.trial_price_tn)}₸ ({int(price_info.trial_price_en)})$ Цена за одну очистку: {int((float.trial_price_tn)/(float(price_info.trial_quantity) + float(price_info.trial_bonus)))}
Тариф: Базовый 
Кол-во очисток : {price_info.beginner_quantity} (бонусных : {price_info.beginner_bonus}), Цена : {price_info.beginner_price_tn}₸ ({int(price_info.trial_price_en)})$ Цена за одну очистку: {int((float.beginner_price_tn)/(float(price_info.beginner_price_tn) + float(price_info.beginner_bonus)))}
Тариф: Продвинутый
Кол-во очисток : {price_info.advanced_quantity} (бонусных : {price_info.advanced_bonus}), Цена : {price_info.advanced_price_tn}₸ ({int(price_info.trial_price_en)})$ Цена за одну очистку: {int((float.trial_price_tn)/(float(price_info.advanced_quantity) + float(price_info.advanced_bonus)))}
Тариф: Топовый 
Кол-во очисток : {price_info.expert_quantity} (бонусных : {price_info.expert_bonus}), Цена : {price_info.expert_price_tn}₸ ({int(price_info.expert_price_en)})$ Цена за одну очистку: {int((float.expert_price_tn)/(float(price_info.expert_quantity) + float(price_info.expert_bonus)))}
''',reply_markup=kb)
        else:
            kb = types.InlineKeyboardMarkup()
            kb.add(bt_1)
            self.bot.send_message(chat_id,"Ещё нету информации",reply_markup=kb)
            
    def send_info(self,chat_id,username):
        kb = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton(text='Назад', callback_data='main_menu')
        kb.add(bt_1)
        email_from_btlog = Bot_logined.objects.filter(nickname=username).first()
        if email_from_btlog:
            get_clear_count = ClearCount.objects.filter(email=email_from_btlog.email).first()
            if get_clear_count:
                self.bot.send_message(chat_id,f'''
Информация об аккаунте {username}
Кол-во очисток : {get_clear_count.count} Бонусных : {get_clear_count.bonus_count} Тариф : {get_clear_count.tarif}
''', reply_markup=kb)
        
    def send_main_menu(self, chat_id, username):
        aut_info = Bot_logined.objects.filter(nickname=username).first()
        if aut_info:
            kb = types.InlineKeyboardMarkup()
            bt_1 = types.InlineKeyboardButton("👤Аккаунт",callback_data='info')
            bt_2 = types.InlineKeyboardButton("📋Тарифы",callback_data='price')
            bt_3 = types.InlineKeyboardButton("✅Очистка",callback_data='clear')
            bt_4 = types.InlineKeyboardButton("Выйти",callback_data='/stop')
            kb.add(bt_1, bt_2, bt_3)
            self.bot.send_message(chat_id, "Здарвствуйте {}🖐🏻".format(username),reply_markup=kb)
        else:
            kb = types.InlineKeyboardMarkup()
            bt_1 = types.InlineKeyboardButton(text='Войти', callback_data='login')
            bt_2 = types.InlineKeyboardButton(text='Пройти регистрацию', url='https://znak.app')
            kb.add(bt_1, bt_2)
            self.bot.send_message(chat_id, "Приветствую, {} чем могу помочь?".format(username), reply_markup=kb)
    def send_login_message(self, chat_id):
        kb = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton(text='Назад', callback_data='main_menu')
        kb.add(bt_1)
        self.bot.send_message(chat_id, 'Введите логин', reply_markup=kb)

    def send_password_message(self,chat_id):
        kb = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton(text='Назад', callback_data='password')
        kb.add(bt_1)
        self.bot.send_message(chat_id, 'Введите пароль', reply_markup=kb)
    
    def update_status(self,chat_id,username):
        clear_info = Bot_logined.objects.filter(nickname=username).first()
        if clear_info.status != False:
            Bot_logined.objects.filter(nickname=username).delete()
            self.bot.send_message(chat_id,"🔒Вы вышли из аккаунта!")
    def run(self):
        self.bot.polling()
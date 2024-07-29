import json  # Добавьте этот импорт в начале файла
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from .models import UserInfo, UserRequests, ClearPrice, Cart, ClearHistory, Payment, ClearCount
import os, sys, time, logging
import zipfile
from datetime import datetime
from .parsers_znakapp.p1.main import main as parsers_img
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import EmailMessage
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from .gen_rfс import xor_encrypt_decrypt
from django.http import JsonResponse, FileResponse
from .webhook import process_json_data
from .tasks import execute_lama, get_active_tasks, delete_task
from celery import current_app
from celery.result import AsyncResult

logger = logging.getLogger(__name__)
# Main dir
base_dir = '/home/djangoapp/znakapp/service'

static_dir = os.path.join(base_dir, 'static')
static_parser_dir = os.path.join(base_dir, 'parsers_znakapp','images')
static_out_dir = os.path.join(base_dir, 'static', 'out')
static_out_users_dir = os.path.join(base_dir, 'static', 'users_out')
mask_path = os.path.join(base_dir, 'lama', 'prepare_masks.py')
lama_path = os.path.join(base_dir, 'lama', 'lama', 'bin', 'predict.py')
python_path = sys.executable

def index(request):
    if request.method == 'POST':
        # Choose form
        if 'form_type' in request.POST:
            if request.POST['form_type'] == 'form1':
                return register_request(request)
            if request.POST['form_type'] == 'form2':
                return user_login(request)
        else:
            if request.user.is_authenticated:
                return render(request, 'service/app.html',{'user_id': request.user.email})
            photos = []
            number = 0
            # Clear IMG after POST request
            input_value = request.POST.get('link_input')
            if input_value:
                number = get_active_tasks()
                result = execute_lama.delay(number, input_value)
                print(f"Lama {number} started")
                task_id = result.id
                while True:
                    task = current_app.AsyncResult(task_id)
                    time.sleep(0.5)
                    if task.status == "SUCCESS":
                        print(f"Thread {number}: OK") 
                        delete_task(number)
                        break
                
                photos = os.listdir(f'{static_out_dir}/s{number}')
                if photos:
                    os.rename(f'{static_out_dir}/s{number}/{photos[0]}', f'{static_out_dir}/s{number}/first_img.png')
                else:
                    pass
                photos[0] = 'first_img.png'
                photos.remove('info_list.txt')

                with open(f'{static_out_dir}/s{number}/info_list.txt', 'r',  encoding='utf-8') as file:
                    data = file.read()
                
                context = data

                return render(request, 'service/index.html', {'photos': photos, 'context': context, 'number': number})
            return render(request, 'service/index.html', {'error': 'Ошибка: исправьте ссылку на объявления'})
    
    if request.user.is_authenticated:
        return render(request, 'service/index.html',{'user_mail': request.user.email})    
  
    return render(request, 'service/index.html')

def price_list(request):
    if request.method == 'POST':
        # Choose form
        if 'form_type' in request.POST:
            if request.POST['form_type'] == 'form1':
                return register_request(request)
            if request.POST['form_type'] == 'form2':
                return user_login(request)
    cart = Cart.objects.first()
    cart_trial = 0.0
    cart_beginer = cart.beginer_price_tn / (cart.beginer_quantity + cart.beginer_bonus)
    cart_advanced = cart.advanced_price_tn/(cart.advanced_bonus+cart.advanced_quantity)
    cart_expert = cart.expert_price_tn/(cart.expert_bonus+cart.expert_quantity)
    if request.user.is_authenticated:
        return render(request, 'service/price.html',{'user_mail': request.user.email, "cart":cart , "cart_trial": cart_trial, "cart_beginer" : cart_beginer, "cart_advanced": cart_advanced, "cart_expert": cart_expert })  
    return render(request, 'service/price.html', {"cart":cart , "cart_beginer" : cart_beginer, "cart_advanced": cart_advanced, "cart_expert": cart_expert, "cart_trial": cart_trial})

def cabinet(request, user_id):
    cart = Cart.objects.first() 
    if request.method == 'POST' and request.user.is_authenticated :
        number = 0
        photos = []

        # Clear IMG after POST request
        input_value = request.POST.get('link_input')
        if input_value:
            number = get_active_tasks.delay()
            result = execute_lama.delay(number, input_value)
            print(f"Lama {number} started")
            task_id = result.id
            while True:
                task = current_app.AsyncResult(task_id)
                time.sleep(1)
                if task.status == "SUCCESS":
                    print(f"Thread {number}: OK") 
                    delete_task(number)
                    break

            # Добавим возврат ID задачи
            response_data = {
                'task_id': str(task_id),
                'status': 'SUCCESS'
            }
            return JsonResponse(response_data)
            
            # Add info for Clear History
            if "kn.kz" in input_value:
                platform = 'www.kn.kz'
            elif "kz.m2" in input_value:
                platform = 'kz.m2bomber.com'
            elif "nedvizhimostpro.kz" in input_value:
                platform = 'nedvizhimostpro.kz'
            elif "olx.kz" in input_value:
                platform = 'olx.kz'  
            elif 'krisha.kz' in input_value:
                platform = "krisha.kz"
            with open(f'{static_out_dir}/s{number}/info_list.txt', 'r') as file:
                params = file.read().strip()
            
            user_id = str(request.user)
            # Save in DB
            new_clear_history = ClearHistory(
                user = user_id,
                platform=platform,
                params=params,
                lot_link = input_value
            )
            new_clear_history.save()
            delete_clear = ClearCount.objects.filter(email=user_id).first()
            if delete_clear:
                ClearCount.objects.filter(email=user_id).update(count=F('count') - 1)
            clear_history_id = str(new_clear_history.id)
            os.mkdir(f'{static_out_users_dir}/{user_id}/{clear_history_id}')
            # Move files
            for img in os.listdir(f'{static_out_dir}/s{number}'):
                os.rename(f'{static_out_dir}/s{number}/{img}', f'{static_out_users_dir}/{user_id}/{clear_history_id}/{img}')

            # Sort out images
            photos = os.listdir(f'{static_out_users_dir}/{user_id}/{clear_history_id}')
            photos.remove('info_list.txt')
            photos.sort()

            with open(f'{static_out_users_dir}/{user_id}/{clear_history_id}/info_list.txt', 'r', encoding='utf-8') as file:
                data = file.read()
            context = data
            user_request = ClearHistory.objects.filter(user=user_id)
            data_from_base = {user_request: user_request}
            tarif_status = ClearCount.objects.filter(email=user_id).first()
            if tarif_status is not None:
                tarif = tarif_status.tarif
                count = tarif_status.count
                bonus_count = tarif_status.bonus_count
                if bonus_count == 0:
                    bonus_count = '0'
                if count == 0:
                    count  = '0'
            return render(request, 'service/app.html', {'user_id': user_id,'tarif':tarif,'count':count,'bonus_count':bonus_count,'photos': photos, 'dt': clear_history_id,'context': context, **data_from_base})
        user_request = ClearHistory.objects.filter(user=user_id)
        data_from_base = {'user_request': user_request}
        return render(request, 'service/app.html', {'user_id': user_id,'error': 'Ошибка: исправьте ссылку на объявления', **data_from_base})

    if request.user.is_authenticated:
        if request.user.email == user_id:
            user_info = UserInfo.objects.filter(user=request.user)
            user_request = UserRequests.objects.filter(user=request.user)
            clear_price = ClearPrice.objects.all()
            for elem in clear_price:
                clear_price = elem.clear_price
            balance = 0
            for elem in user_info:
                balance = elem.balance / clear_price
            tarif_status = ClearCount.objects.filter(email=user_id).first()
            tarif = "Пробный" #default
            count = 3 #default
            
            if tarif_status is not None:
                tarif = tarif_status.tarif
                count = tarif_status.count
                bonus_count = tarif_status.bonus_count
                if bonus_count == 0:
                    bonus_count = '0'
                if count == 0:
                    count  = '0'
            return render(request, 'service/app.html',
                        {'user_id': user_id,'tarif':tarif,'count':count,'bonus_count':bonus_count,'user_info': int(balance), 'user_request': user_request, 'cart': cart})
        else:
            return redirect('homepage')
    else:
        return redirect('homepage')

@csrf_protect
def user_login(request):
    email = request.POST.get('email')  # Получаем значение поля email из POST-запроса
    password = request.POST.get('password')  # Получаем значение поля password из POST-запроса
    
    user = authenticate(username=email, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('cabinet', user_id=user.username)
        else:
            log_error_msg = 'Ваш аккаунт не подтверждён, проверьте почту'
            return render(request, 'service/index.html', {'log_error_msg': log_error_msg})
    else:
        log_error_msg = 'Проверьте логин и пароль и попробуйте еще раз.'
        return render(request, 'service/index.html', {'log_error_msg': log_error_msg})
        #return render(request, 'service/index.html/', {'error_msg': error_msg})

@csrf_protect
def register_request(request):
    reg_error_msg = ''
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_repeat = request.POST.get('password_repeat')
    validate = False
    if  password != password_repeat:
        reg_error_msg = 'Пароли не совпадают'
    else:
       validate = True 
    
    if validate:  
        try:      
            user = User.objects.create_user(username=email, email=email, password=password)
            print("Пользователь создан")
            clear_email = email
            clear_count = 3
            clear_bonus_count = 0
            clear_tarif = 'Пробный'
            user_clear_count = ClearCount.objects.create(email=clear_email,count=clear_count,tarif=clear_tarif,bonus_count=clear_bonus_count)
            print("Очистки добавлены")
        except Exception as ex:
            print(ex)
            reg_error_msg = "Пользователь с данным адресом электронной почты уже зарегистрирован"
            return render(request, "service/index.html", {"reg_error_msg": reg_error_msg})
        try:
            serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
            token = serializer.dumps(user.id)
            confirm_url = request.build_absolute_uri(reverse('confirm_email', kwargs={'token': token}))
        except Exception as ex:
            print(ex) 
        try:
            email = EmailMessage(
                'Подтверждение почты',
                f'Перейдите по ссылке для подтверждения почты: {confirm_url}',
                'reg.znak.app@mail.ru',
                [user.email]
            )
            user.is_active = False
            user.save()
            user_clear_count.save()
            email.send()
        except Exception as ex:
            print(ex)
            reg_error_msg = "Проверьте адрес электронной почты"
            return render(request, "service/index.html", {"reg_error_msg": reg_error_msg})
    
        try:
            os.mkdir(f'{static_dir}/users_out/{user}')
        finally:
            info_msg = """Мы отправили вам на указанную почту письмо с ссылкой для подтверждения. Проверьте почту от нас к вам уже пришло письмо, 
            пройдите по ссылке для завершения регистрации. Если письма нет, проверьте папку Спам. Возможно письмо попало туда. """
            return render(request,"service/mail_info.html", {"info_msg": info_msg,"user_mail": user.username})
    reg_error_msg = 'Произошла ошибка при регистрации пользователя'
    return render(request, "service/index.html", {"reg_error_msg": reg_error_msg})

def confirm_email(request, token):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        user_id = serializer.loads(token, max_age=3600)  # Проверка подписи и срока действия ссылки
        user = User.objects.get(id=user_id)
        user.is_active = True  # Активация пользователя
        user.save()
        info_msg = 'Почта подтверждена. Регистрация завершена.'
    except:
        info_msg = 'Ссылка для подтверждения недействительна или истек срок действия.'
    finally:
        return render(request,"service/mail_info.html", {"info_msg": info_msg,"user_mail": user.username})

def user_logout(request):
    logout(request)
    return redirect("homepage")


def download_images(request, user_id, element_id):
    if request.user.is_authenticated:
        user_id = str(request.user)
        static_out_users_imgs_dir = static_dir + '/users_out/' + user_id + f'/{element_id}/'

        # Получаем список файлов в последней директории
        files = os.listdir(static_out_users_imgs_dir)

        # Создаем архив
        temp_zip_path = static_dir + 'images.zip'  # Замените на путь, куда вы хотите сохранить архив
        with zipfile.ZipFile(temp_zip_path, 'w') as zipf:
            for file in files:
                file_path = os.path.join(static_out_users_imgs_dir, file)
                zipf.write(file_path, arcname=file)

        # Отправляем архив в ответе
        with open(temp_zip_path, 'rb') as zipf:
            response = HttpResponse(zipf.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="images.zip"'
            return response

@csrf_exempt
def process_webhook(request):
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        body = request.body.decode('utf-8')
        logger.info(f'Received webhook with Content-Type {content_type}: {body}')
        try:
            json_data = request.body.decode('utf-8')
            process_json_data(json_data)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f'Error processing webhook: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return HttpResponse("<h1>Json не поступал</h1>", status=405)


def price_cabinet(request, user_id):
    cart = Cart.objects.first() 
    cart_trial = 0.0
    cart_beginer = cart.beginer_price_tn / (cart.beginer_quantity + cart.beginer_bonus)
    cart_advanced = cart.advanced_price_tn/(cart.advanced_bonus+cart.advanced_quantity)
    cart_expert = cart.expert_price_tn/(cart.expert_bonus+cart.expert_quantity)
    return render(request, 'service/price_cabinet.html', {"user_id": user_id,"cart":cart , "cart_beginer" : cart_beginer, "cart_advanced": cart_advanced, "cart_expert": cart_expert, "cart_trial": cart_trial})

def partner(request, user_id):
    ref_url = str(request.build_absolute_uri(reverse('homepage')) + xor_encrypt_decrypt(request.user.username, "secret_key"))
    return render(request, 'service/partner.html',{"user_id": user_id, "ref_url" : ref_url})

def history(request, user_id):
    user_request = ClearHistory.objects.filter(user=user_id)
    data_from_base = {'user_request': user_request}
    return render(request, 'service/history.html',{"user_id": user_id, 'user_request': user_request, **data_from_base})

@csrf_protect
def profile(request, user_id):
    if request.method == 'POST':
        new_mail = request.POST.get('email')
        print(new_mail)
        if new_mail:
            request.user.email = new_mail
            request.user.usermail = new_mail
            os.rename(f'{static_out_users_dir}/{user_id}', f'{static_out_users_dir}/{new_mail}')
            request.user.save()
        # изменить название папки
    return render(request, 'service/profile.html',{"user_id": user_id})

def tg_info(request):
    if request.method == 'POST':
        # Choose form
        if 'form_type' in request.POST:
            if request.POST['form_type'] == 'form1':
                return register_request(request)
            if request.POST['form_type'] == 'form2':
                return user_login(request)
    info_msg = "Наш telegram бот"
    if request.user.is_authenticated:
        return render(request, 'service/tg_info.html',{'user_mail': request.user.email, "info_msg": info_msg})  
    return render(request, 'service/tg_info.html', {"info_msg": info_msg})

def api_info(request):
    if request.method == 'POST':
        # Choose form
        if 'form_type' in request.POST:
            if request.POST['form_type'] == 'form1':
                return register_request(request)
            if request.POST['form_type'] == 'form2':
                return user_login(request)
    info_msg = """Наше API открывает перед вами возможность 
                интегрировать и персонализировать наше приложение в соответствии с вашими 
                уникальными потребностями. Пользуйтесь API для удобного доступа к данным, 
                автоматизации задач и создания индивидуальных решений, делая ваш опыт 
                использования приложения еще более эффективным."""
    if request.user.is_authenticated:
        return render(request, 'service/tg_info.html',{'user_mail': request.user.email, "info_msg": info_msg})  
    return render(request, 'service/tg_info.html', {"info_msg": info_msg})

def api_cabinet(request, user_id):
    return render(request, 'service/api_cabinet.html', {'user_id': user_id})

def open_photos(request, user_id, element_id):
    user_request = ClearHistory.objects.filter(user=user_id)
    data_from_base = {'user_request': user_request}
    
    photos = os.listdir(f'{static_out_users_dir}/{user_id}/{element_id}')
    photos.sort()
    photos.remove('info_list.txt')
    with open(f'{static_out_users_dir}/{user_id}/{element_id}/info_list.txt', 'r', encoding='utf-8') as file:
        data = file.read()
        context = data
    return render(request, 'service/history.html',{"user_id": user_id, 'photos': photos, 'dt': element_id,'context': context, 'user_request': user_request, **data_from_base})

def download_image(request,user_id,filename,clear_history_id):
    photo_path = f"{static_out_users_dir}/{user_id}/{clear_history_id}/{filename}"
    if os.path.exists(photo_path):
        print(photo_path)
        response = FileResponse(open(photo_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="photo.jpg"'
        return response
    else:
        # Обработка ситуации, когда файл не найден
        return HttpResponse("Фото не найдено", status=404)

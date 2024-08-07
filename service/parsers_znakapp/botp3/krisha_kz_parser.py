import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
from PIL import Image
import os, sys, subprocess

base_dir = '/home/djangoapp/znakapp/service'
python_path = sys.executable
mask_path = os.path.join(base_dir,'lama','bot3','prepare_masks.py')
mask_id_path = os.path.join(base_dir,'lama','bot3','prepare_masks_id.py')
static_out_dir =  os.path.join(base_dir, 'parsers_znakapp','botp3', 'images')
txt_out_dir = os.path.join(base_dir, 'parsers_znakapp','botp3')
options = Options()

options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
options.add_argument("--headless")  # Запуск Chrome в режиме без головы
options.add_argument("--no-sandbox")  # Отключение режима песочницы для работы в изолированном окружении
options.add_argument("--disable-dev-shm-usage")  # Отключение использования общей памяти для предотвращения проблем с производительностью
options.add_argument("--disable-gpu")  # Отключение аппаратного ускорения, полезно для режима без головы
options.add_argument("--window-size=1920,1080")  # Задание размера окна
options.add_argument("----enable-automation")
options.add_argument("--disable-extensions")

try:
    driver = webdriver.Chrome(options=options)
except Exception as ex:
    print(f'{ex}')
def parsing_krisha_kz(link):
    try:
        driver.get(link)
        response = requests.get(link).text
        soup = BeautifulSoup(response,'lxml')
        close_modal = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/main/div[2]/div/div[1]/div/div/div[1]/div/button')))
        close_modal.click()
        try:
            check_owner = soup.find('div',class_='owners__name owners__name--large').text #Проверка на владельца (Хозяин недвижимости)
            print(check_owner)
        except:
            check_owner = 0
        imgs_src_list = soup.find_all('div', class_='gallery__small-item')
        count_of_click = len(imgs_src_list) - 1 # кол-во кликов в модальном окне, где у нас фотка
        print(count_of_click)
        first_img_to_click = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'gallery__small-item')))
        first_img_to_click.click() # Открытие модального окна
        time.sleep(1)
        i = 0
        download_links = [] # список, куда будут заноситься ссылки наши на скачивание изображения
        while i <= count_of_click:
            image_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div/div/img")))
            download_links.append(image_link.get_attribute('src'))
            #next_img = driver.find_element(By.XPATH,'/html/body/div[6]/div/div/div/a[2]')
            next_img = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div/a[2]")))
            next_img.click()
            time.sleep(0.5)
            i+=1
        for i in download_links: # Идём по ссылкам и качаем фотки
            time.sleep(0.5)
            image_bytes = requests.get(i).content
            with open(f'{static_out_dir}/img{download_links.index(i)}.png', 'wb') as file:
                file.write(image_bytes)
        driver.close()
        driver.quit()
        directory = static_out_dir
        for filename in os.listdir(directory): # изменяем размер
            if filename.endswith(".png"):
                image_path = os.path.join(directory,filename)
                image = Image.open(image_path)
                width, height = image.size
                if height > width:
                    new_height = 675
                    new_width = 900
                    resize_image = image.resize((new_height,new_width),Image.BILINEAR)
                    resize_image.save(os.path.join(directory,f"new_{filename}"))
                else:
                    new_height = 1200
                    new_width = 900
                    resize_image = image.resize((new_height,new_width),Image.BILINEAR)
                    resize_image.save(os.path.join(directory,f"new_{filename}"))

        offer_info = soup.find('div', class_='offer__advert-title').find('h1').text.strip()
        print(offer_info)

        with open(f'{txt_out_dir}/info_list.txt', 'w', encoding='utf-8') as file:
            file.write(f'{offer_info}')

        # Получаем список файлов в директории
        files = os.listdir(directory)

        # Удаляем файлы, соответствующие заданному шаблону
        for file in files:
            if file.startswith('img') and file.endswith('.png'):
                os.remove(os.path.join(directory, file))
        # удаляем фотки, и выбираем потом нужную маску
        
        if check_owner==0:
            subprocess.call([python_path, mask_path])
        else:
            subprocess.call([python_path, mask_id_path])
        print(f'Mask bot 1: OK')
        
    except Exception as ex:
        print(f"Error link : {ex}")
        driver.close()
        driver.quit()
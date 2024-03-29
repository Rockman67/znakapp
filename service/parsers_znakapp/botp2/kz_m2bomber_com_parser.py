import requests
from bs4 import BeautifulSoup


static_out_dir = '/home/djangoapp/znakapp/service/parsers_znakapp/botp2/images'
txt_out_dir = '/home/djangoapp/znakapp/service/parsers_znakapp/botp2'


def parsing_kz_m2bomber(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    imgs_src_list = soup.find_all('div', class_='fullcard-big-slider')
    img_href = ' '.join(map(str, imgs_src_list))
    img_href = img_href.split('\n')
    img_href = img_href[1:-1]
    counter = 1
    try:
        for elem in img_href:
            image_bytes = requests.get(f'https://kz.m2bomber.com/{elem}').content
            with open(f'{static_out_dir}/img{counter}.jpeg', 'wb') as file:
                file.write(image_bytes)
            counter += 1
        h1_name = soup.find('address', class_='fullcard-address').text
        tags = soup.find('ul', class_='fullcard-tags').find_all('li')
        param_list = []
        param_list.append(h1_name)
        for elem in tags:
            if 'поднять в Топ' not in elem.text:
                param_list.append(elem.text.strip())
        total_price = soup.find(id='priceValueHolder').text.strip()
        info_list = [f'Город: {param_list[0]}',
              f'Площадь, м²: {param_list[1]}',
              f'Кол-во комнат: {param_list[2]}',
              f'Этаж: {param_list[3]}',
              f'Цена: {total_price}']

        with open(f'{txt_out_dir}/info_list.txt', 'w') as file:
            for item in info_list:
                file.write("%s\n" % item)
    except Exception as ex:
        print(f'Save error')


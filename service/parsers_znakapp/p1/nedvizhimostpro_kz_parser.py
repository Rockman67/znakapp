import requests
from bs4 import BeautifulSoup

static_out_dir = '/home/djangoapp/znakapp/service/parsers_znakapp/p1/images'
txt_out_dir = '/home/djangoapp/znakapp/service/parsers_znakapp/p1'

def parsing_nevdizhimostpro_kz(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    imgs_src_link = soup.find_all('a', {"data-fancybox": "gallery"})

    counter = 1
    for elem in imgs_src_link:
        img_href = str(elem)
        img_href = img_href[img_href.find('/uploads'):img_href.find('.jpg')+4]
        img_bytes = requests.get(f'https://nedvizhimostpro.kz/{img_href}').content
        with open(f'{static_out_dir}/img{counter}.webp', 'wb') as file:
            file.write(img_bytes)
        counter += 1

        additional_info = soup.find('div', class_="additional_details").find_all('span')
        details = []
        for elem in additional_info:
            details.append(elem.text)

    info_list = [
          f'Этаж: {details[2]}',
          f'Цена: {details[3]}',
          f'Площадь: {details[4]}',
          ]

    with open(f'{txt_out_dir}/info_list.txt', 'w') as file:
        for item in info_list:
            file.write("%s\n" % item)
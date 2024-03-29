import requests
from bs4 import BeautifulSoup


static_out_dir = '/home/djangoapp/znakapp/service/parsers_znakapp/botp1/images'
txt_out_dir = '/home/djangoapp/znakapp/service/parsers_znakapp/botp1'

# def parsing_kn_kz(link):
def parsing_kn_kz(link):
    try:
        link = str(link)
        if 'm.kn.kz' in link:
            str(link.replace('m.kn.kz', 'www.kn.kz', 1))
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        imgs_src_list = soup.find_all('div', class_='image-item')
        counter = 1
        for elem in imgs_src_list:
            img_href = str(elem)
            img_href = img_href[img_href.find('/uploads'):img_href.find('.jpg')+4]
            image_bytes = requests.get(f'https://www.kn.kz{img_href}').content
            with open(f'{static_out_dir}/img{counter}.webp', 'wb') as file:
                file.write(image_bytes)
            counter += 1
        name = soup.find('h1').text
        td = soup.find_all('td')
        param_list = []
        for elem in td:
             param_list.append(elem.getText().strip())

        total_price = soup.find('span', class_='price').text.strip()

        info_list = [f'{name},\n',
              f'Улица: {param_list[0]},',
              f'Количество комнат: {param_list[2]},',
              f'Этаж: {param_list[3]},',
              f'Площадь: {param_list[4]},',
              f'Цена: {total_price}'
              ]
        with open(f'{txt_out_dir}/info_list.txt', 'w') as file:
            for item in info_list:
                file.write("%s\n" % item)
    except Exception as ex:
        print(ex)

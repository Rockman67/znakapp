import requests
from bs4 import BeautifulSoup


static_out_dir = '/home/djangoapp/znakapp/service/parsers_znakapp/botp3/images'
txt_out_dir = '/home/djangoapp/znakapp/service/parsers_znakapp/botp3'

def parsing_olx_kz(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    imgs_src_list = soup.find_all('div', class_='swiper-zoom-container')
    counter = 1
    try:
        for elem in imgs_src_list:
            img_href = str(elem)
            img_href = img_href[img_href.find('https'):img_href.find('992w')]
            img_href = img_href[img_href.find('780w, ')+6:-1]
            image_bytes = requests.get(img_href).content
            with open(f'{static_out_dir}/img{counter}.jpeg', 'wb') as file:
                file.write(image_bytes)
            counter += 1
        info = soup.find('div', {'data-cy': 'ad_description'})
        price = soup.find('div', {'data-testid': 'ad-price-container'})
        info_list = [f'Цена: {price.text}', f'{info.text}']
        with open(f'{txt_out_dir}/info_list.txt', 'w') as file:
            for item in info_list:
                file.write("%s\n" % item)
    except Exception as ex:
        print(f'Save error {ex}')




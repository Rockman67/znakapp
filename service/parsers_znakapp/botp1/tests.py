import requests
from bs4 import BeautifulSoup


link = 'https://krisha.kz/a/show/683209777'
response = requests.get(link)
soup = BeautifulSoup(response.text, 'lxml')
offer_info = soup.find_all('div', class_='offer__info-title')
offer__advert_short_info = soup.find_all('div', class_='offer__advert-short-info')
info_list = []
param_list = []
for elem in offer_info:
  if elem != '\n' or '':
        info_list.append(elem.text)

for elem in offer__advert_short_info:
      if elem != '\n' or '':
            param_list.append(elem.text)

param_list[0] = param_list[0][:param_list[0].find('показать на карте')]
for i in range(len(offer_info)):
      print(f'{info_list[i]}: {param_list[i]}')


import requests
import lxml
from bs4 import BeautifulSoup
import csv
url = 'https://www.banki.ru/services/responses/list/'
#находит спиок ссылок, проходит по ним и собирает полный текст

def parce(url):
    responce = requests.get(url)
    soup = BeautifulSoup(responce.text,'lxml')
    contain = soup.select('#responses-list-app')
    property_info = []
    for container in contain:
        # названия заголовков

        title = [x.get_text().rstrip() for x in soup.find_all('a',class_='font-size-large font-bold')]
        title = ';'.join(title)

        # в классе рейтинг последние цифры разные используй re
        #сделал огромный костыль потому что пока не оч знаю bs & css
        rating = container.find_all('span', class_ = ['rating-grade rating-grade--small rating-grade--hollow rating-grade--value-1','rating-grade rating-grade--small rating-grade--hollow rating-grade--value-2',
                                                      'rating-grade rating-grade--small rating-grade--hollow rating-grade--value-3','rating-grade rating-grade--small rating-grade--hollow rating-grade--value-4','rating-grade rating-grade--small rating-grade--hollow rating-grade--value-5'])
        rating = [x.get_text(strip=True) for x in rating]
        rating = ';'.join(rating)

        bank_name = [x.get_text().strip() for x in soup.find_all('span', class_='link-with-icon__text color-link')]
        bank_name = ';'.join(bank_name)

        datetime = [x.get_text().strip().split(' ')[0] for x in soup.find_all('time', class_='display-inline-block')]
        datetime = ';'.join(datetime)

# копируем полный текст сообщения

        mes = soup.select('.responses__item__message')
        full_message = []
        for message in mes:
            message = [message['href'] for message in message.find_all('a', href=True)]

            x = 'https://www.banki.ru'
            urlib = []
            for urll in message:
                urlib.append(x + urll)
                #  print(urlib)

            for href in urlib:
                # print(href)
                href_responce = requests.get(href)
                soup = BeautifulSoup(href_responce.text, 'lxml')
                full_m = [x.get_text().strip() for x in soup.find_all('div', class_='article-text response-page__text markup-inside-small markup-inside-small--bullet')]
                full_m = ';'.join(full_m)
                full_message.append(full_m)

        full_message = ';'.join(full_message)

        property_info.append({ 'название':title,
            'оценка':rating,
            'банк':bank_name,
            'дата':datetime,
            'сообщение':full_message

        })
    return property_info

def writerCSVHeader ():
    with open ('banki_example.csv', 'a',newline='',encoding="utf-8") as file:
        open_file = csv.writer(file)
        open_file.writerow(('title','rating','bank_name','date','message'))

def files_writer (property):
    with open ('banki_example.csv', 'a',newline='',encoding="utf-8") as file:
        open_file = csv.writer(file)
        #property_info = parce(url)
        for property in property:
            open_file.writerow((property['название'],property['оценка'],property['банк'],property['дата'],property['сообщение']))

if __name__ == '__main__':
    writerCSVHeader() #записываем заголовки
    for x in range(1,17):
        print(f'Скачивается:{x} из {16}' )
        url = f'https://www.banki.ru/services/responses/list/?page={x}&isMobile=0'
        files_writer(parce(url))



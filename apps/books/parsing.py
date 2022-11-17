import json
import requests
from bs4 import BeautifulSoup
from bs4 import Tag, ResultSet

from genre import ROMAN, FANTASY, CYBERPUNK, ABC, THRILLER


HOST = 'https://www.litmir.me'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


def get_db(db):
    with open(f'{db}.JSON', 'r') as file:
        return json.load(file)


def write_db(data, db):
    with open(f'{db}.JSON', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    

def get_html(url: str, headers: dict='', params: str=''):
    """ Функция для получения html кода """
    html = requests.get(
        url,
        headers=headers,
        params=params,
        verify=False
    )
    return html.text


def get_card_from_html(html: str) -> ResultSet:
    soup = BeautifulSoup(html, 'lxml')
    cards: ResultSet = soup.find_all('table', class_='island')
    return cards

def get_photo(cards):
    result = []
    for card in cards:
        photo = HOST + card.find('td', class_='lt22').find('a').find('img').get('data-src')
        result.append(photo)
    return result



def get_author(cards):
    result = []
    for card in cards:
        author = card.find('span', class_='desc2').text.strip()
        result.append(author)
    return result

def get_page(cards):
    result = []
    NUMBER = 0
    for card in cards:
        pages = card.find_all('span', class_='desc2')
        for page in pages:
            num = page.text.strip()
            if len(num) < 4:
                result.append(num)
    return result


def get_title(cards):
    result = []
    for card in cards:
        title = card.find('div', class_='book_name').text 
        result.append(title)
    return result

def parse_data_from_cards(cards):
    result = []
    num = 0
    page = get_page(cards)
    for card in cards:
        title = card.find('div', class_='book_name').text 
        author = card.find('span', class_='desc2').text.strip()
        photo = HOST + card.find('td', class_='lt22').find('a').find('img').get('data-src')
        desc = card.find('div', class_='BBHtmlCodeInner').text.replace('\"', '').replace('\n', '')
        obj = {
            'title': title,
            'photo': photo,
            'author': author,
            'page': page[num],
            'desc': desc
        }
        num +=1
        result.append(obj)
    return result


if __name__ == '__main__':
    html = get_html(THRILLER) 
    cards = get_card_from_html(html)
    parse = parse_data_from_cards(cards)
    write_db(parse,'THRILLER')





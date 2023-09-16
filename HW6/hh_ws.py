
from urllib.parse import urljoin
import fake_headers
import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint
import json
import keyboard


## КОНСТАНТЫ:
KEYWORDS = ["Django", "Flask"]
SITE = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
SITE_MAIN = "https://spb.hh.ru"
OUT_FILE_NAME = 'vacancies.json'

## ОПЦИИ
MAX_PAGES = 20        # Макс. количество обрабатываемых страниц или 0=ВСЕ
PRINT_VAC = 1         # Вывод на экран


err_cnt = 0           # Счетчик ошибок


def exceptor(func):
    def __wrapper (*args, **kwargs):
        global err_cnt
        try:
            return func(*args, **kwargs)
        except:
            print (f'---- Произошла ошибка в функции "{func.__name__}()"\n')
            err_cnt += 1
            return None
    return __wrapper



@exceptor
def get_soup(request):
    headers_gen = fake_headers.Headers(browser="chrome", os="win")
    response = requests.get(request, headers=headers_gen.generate())
    html_data = response.text
    return BeautifulSoup(html_data, "lxml")


@exceptor
def vacancy_data(link, keywords=None):
    soup = get_soup(link)
    if not soup:
        return None

##    desc = soup.find("div", class_="main-content")
    desc = soup.find("div", class_="vacancy-description")
##    desc = soup.find("div", attrs = {"data-qa": "vacancy-description"})

    result = None

    if desc:
        key_str = desc.find(string = keywords)
        if key_str:
            company = soup.find("a", attrs = {"data-qa": "vacancy-company-name"})
            company = company.find("span").text

            salary = soup.find("span", attrs = {"data-qa": "vacancy-salary-compensation-type-net"})
            salary = salary.text if salary else 'ЗП засекречена'

            city = soup.find("p", attrs = {"data-qa": "vacancy-view-location"})
            if not city:
                city = soup.find("span",  attrs = {"data-qa": "vacancy-view-raw-address"})
            city = city.text if city else 'Город не обнаружен'

            result = {
                "salary" : salary,
                "company" : company,
                "city" : city,
                "keystr": key_str
            }

    return result




if __name__ == '__main__':

    keywords = '|'.join(KEYWORDS)
    print(keywords)
    re_keywords = re.compile(keywords, flags=re.IGNORECASE)

    site = SITE
    page = 0
    data = []
    err_cnt = 0
    app_terminate = False

    while (page < MAX_PAGES or MAX_PAGES == 0) and not app_terminate:
        soup = get_soup(site)
        if not soup:
            continue

        vacancy_list_tag = soup.find("main", class_="vacancy-serp-content")
        if not vacancy_list_tag:
            break

        vacancy_tags = vacancy_list_tag.find_all("a", class_="serp-item__title" )

        page += 1
        print(f"\n======= page {page} =======\n")

        for vtag in vacancy_tags:
            link = vtag.attrs['href']
            title = vtag.text

            res = vacancy_data(link, re_keywords)
            if res:
                res["title"] = title
                res["link"] = link[:(str(link).find('?'))]
                if PRINT_VAC:
                    print(res["title"])
                    print(res["link"])
                    print(res["salary"])
                    print(res["company"])
                    print(res["city"])
                    print()
                data.append(res)

            if keyboard.is_pressed('q'):
                print('Прерывание работы')
                app_terminate = True
                break
##                exit()

        next_page = soup.find("a", attrs = {"data-qa": "pager-next"})
        if next_page:
            site = urljoin(SITE_MAIN, next_page.attrs['href'])
        else:
            break

    jdata = {'keywords':keywords, 'vacancies':data}
    with open(OUT_FILE_NAME, 'w', encoding='UTF-8') as file:
        json.dump(jdata, file, ensure_ascii=False, indent=4)

##    pprint(jdata)

    print (f'Сохранено {len(data)} вакансий c {page} страниц в файл "{OUT_FILE_NAME}"')
    print (f'Ошибок {err_cnt}')



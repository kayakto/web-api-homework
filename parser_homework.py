import requests
from bs4 import BeautifulSoup


# находит все названия и цены на кружки
# принимает url максидома и путь до категории
def find_name_and_price(base_url, start_path):
    # полный url для 1 страницы из категории
    url = base_url + start_path
    # словарь, в котором ключ - название товара, значение - цена товара
    result = {}
    # пока url не None
    while url:
        # получаем страницу с кружками
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        # массив article, в каждом - товар, его описание и цена
        articles = soup.find_all("article", class_="l-product")
        # для каждого товара
        for article in articles:
            # название товара
            name = article.find("span", itemprop="name")
            # цена товара
            price = article.find("span", itemprop="price")
            # заполняем словарь
            result[name.text] = int(price.text)

        # ищем ссылку на следующую страницу с товарами
        next_page = soup.find("a", id="navigation_2_next_page")
        # если ссылка найдена
        if next_page:
            # полный url на следующую страницу
            url = base_url + next_page["href"]
        # иначе выходим из цикла (ссылки нет)
        else:
            url = None

    # возвращаем словарь с названиями и ценами на товары
    return result


# url максидома
base_url = "https://www.maxidom.ru/"
#  путь до категории "кружки"
start_path = "catalog/kruzhki/"

# словарь с названиями и ценами всех кружек, которые есть на сайте
elements = find_name_and_price(base_url, start_path)
# вывод содержимого словаря
for name, price in elements.items():
    print(f"Название: {name}, Цена: {price} ₽/шт")

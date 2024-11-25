import csv
import json
from requests import get
from lxml.html import fromstring

# Список для хранения данных о продуктах
product_list = []

# Параметры для парсинга страниц с 1 по 5
base_url = "https://www.gintarine.lt/maistas-ir-papildai-sportininkams?page={}"

# Проходим по всем страницам от 1 до 5
for page in range(1, 6):
    # Формируем URL для текущей страницы
    url = base_url.format(page)

    # Получаем HTML содержимое страницы
    response = get(url)
    html_content = response.text

    # Парсим HTML
    tree = fromstring(html_content)

    # Получаем все товарные позиции
    products = tree.xpath("//div[contains(@class, 'product-item')]")

    for product in products:
        product_name = product.xpath(".//input[@name='productName']/@value")[0]
        product_price = product.xpath(".//input[@name='productPrice']/@value")[0]
        product_brand = product.xpath(".//input[@name='productBrand']/@value")[0]

        # Сохраняем данные в словарь
        product_data = {
            "Product Name": product_name,
            "Product Price": product_price,
            "Product Brand": product_brand
        }

        product_list.append(product_data)

# Записываем данные в CSV файл
with open("products.csv", "w", newline='', encoding='utf-8') as csv_file:
    fieldnames = ["Product Name", "Product Price", "Product Brand"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(product_list)

# Записываем данные в JSON файл
with open("products.json", "w", encoding='utf-8') as json_file:
    json.dump(product_list, json_file, ensure_ascii=False, indent=4)

print("Данные успешно сохранены в products.csv и products.json.")
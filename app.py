from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}

def flipkart(name):
    try:
        name1 = name.replace(" ", "+")
        url = f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        if soup.select('._4rR01T'):
            flipkart_name = soup.select('._4rR01T')[0].getText().strip()
            flipkart_price = soup.select('._30jeq3')[0].getText().strip()
            return flipkart_name, flipkart_price, url
        elif soup.select('.s1Q9rs'):
            flipkart_name = soup.select('.s1Q9rs')[0].getText().strip()
            flipkart_price = soup.select('._30jeq3')[0].getText().strip()
            return flipkart_name, flipkart_price, url
    except:
        return "No product found", "0", url
    return "No product found", "0", url

def amazon(name):
    try:
        name1 = name.replace(" ", "-")
        name2 = name.replace(" ", "+")
        url = f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')

        if amazon_page:
            amazon_name = amazon_page[0].getText().strip()
            amazon_price = soup.select('.a-price-whole')[0].getText().strip()
            return amazon_name, amazon_price, url
    except:
        return "No product found", "0", url
    return "No product found", "0", url

def convert(price_str):
    return int("".join(filter(str.isdigit, price_str)))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form['product_name']
        flipkart_name, flipkart_price, flipkart_url = flipkart(product_name)
        amazon_name, amazon_price, amazon_url = amazon(product_name)

        flipkart_price_val = convert(flipkart_price) if flipkart_price != "0" else None
        amazon_price_val = convert(amazon_price) if amazon_price != "0" else None

        prices = {
            'Flipkart': {'name': flipkart_name, 'price': flipkart_price, 'url': flipkart_url},
            'Amazon': {'name': amazon_name, 'price': amazon_price, 'url': amazon_url}
        }

        return render_template('index.html', prices=prices, product_name=product_name)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_author_about(author_url):
    response = requests.get("https://quotes.toscrape.com" + author_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    about = soup.find('div', class_='author-description').text.strip()
    return about

def scrape_quotes():
    base_url = "https://quotes.toscrape.com"
    current_page = "/page/1/"
    quotes = []

    while current_page:
        response = requests.get(base_url + current_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            author_url = quote.find('a')['href']
            about = get_author_about(author_url)
            quotes.append({'text': text, 'author': author, 'tags': tags, 'about': about})
        
        next_button = soup.find('li', class_='next')
        if next_button:
            current_page = next_button.find('a')['href']
        else:
            current_page = None

    return pd.DataFrame(quotes)

if __name__ == "__main__":
    df = scrape_quotes()
    print(df)
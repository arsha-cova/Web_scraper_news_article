import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_news_article(url):
    response = requests.get(url)

    # Ensure the request was successful
    if response.status_code != 200:
        return f"Error: Unable to fetch the webpage. Status code: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title
    title_element = soup.find('h1', class_='sc-518485e5-0 bWszMR')
    title = title_element.get_text(strip=True) if title_element else "Title not found"

    # Extract the author's name using the CSS selector
    author_element = soup.select_one('html > body > div:nth-of-type(2) > div > main > article > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div > span')
    author = author_element.get_text(strip=True) if author_element else "Author not found"

    # Find all div elements with the class that contains the time element
    div_elements = soup.find_all('div')
    print("#########",div_elements)
    # Iterate over each div element and find the time element inside it
    publication_time = None
    for div in div_elements:
        time_element = div.find('time', class_='sc-2b5e3b35-2 fkLXLN')
        if time_element:
            publication_time = time_element.get_text(strip=True)
    article_info = (
        f"Title: {title}\n"
        f"Author: {author}\n"
        f"Publication Time: {publication_time}\n"

    )
    return article_info


"""    # Extract all paragraph text
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p', class_='sc-eb7bd5f6-0 fYAfXe')]
    text = "\n".join(paragraphs) if paragraphs else "No article content found"

    # Record the current scraping time
    scraping_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Combine all extracted information
    article_info = (
        f"Title: {title}\n"
        f"Author: {author}\n"
        f"Publication Time: {publication_time}\n"
        f"Scraping Time: {scraping_time}\n\n"
        f"{text}"
    )
    """

if __name__ == "__main__":
    url = 'https://www.bbc.com/news/articles/c4gzn4xx0q2o'
    print(scrape_news_article(url))

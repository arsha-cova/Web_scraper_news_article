import requests
from bs4 import BeautifulSoup
import textwrap
import argparse  # For handling command-line arguments


def scrape_news_article(url):
    response = requests.get(url)

    # Ensure the request was successful
    if response.status_code != 200:
        return f"Error: Unable to fetch the webpage. Status code: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title
    title_element = soup.find('h1', class_='article-hero-headline__htag lh-none-print black-print')
    title = title_element.get_text(strip=True) if title_element else "Title not found"

    # Extract the subtitle (dek)
    subtitle_element = soup.find('div', class_='styles_articleDek__Icz5H styles_withImage__SSIip',
                                 attrs={'data-testid': 'article-dek'})
    subtitle = subtitle_element.get_text(strip=True) if subtitle_element else "Subtitle not found"

    # Extract the published date (text)
    date_element = soup.find('time', {'data-testid': 'timestamp__datePublished'})
    published_date = date_element.get_text(strip=True) if date_element else "Published date not found"

    # Extract the author
    author_element = soup.find('span', {'data-testid': 'byline-name'})
    author = author_element.get_text(strip=True) if author_element else "Author not found"

    # Find all <p> tags inside the div with class "article-body__content"
    article_body = soup.find('div', class_='article-body__content')
    paragraphs = article_body.find_all('p')

    # Wrap each paragraph individually
    wrapped_paragraphs = []
    for paragraph in paragraphs:
        paragraph_text = paragraph.get_text(strip=True)
        wrapped_paragraph = textwrap.fill(paragraph_text, width=120)
        wrapped_paragraphs.append(wrapped_paragraph)

    # Combine wrapped paragraphs with two newlines between them
    article_text = "\n\n".join(wrapped_paragraphs)

    article_info = (
        f"Title: {title}\n"
        f"Subtitle: {subtitle}\n"
        f"Author: {author}\n"
        f"Published date: {published_date}\n"
        f"Article text:\n{article_text}\n"
    )
    return article_info


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Scrape a news article from the given URL.")
    parser.add_argument('url', type=str, help="The URL of the news article to scrape.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the scrape function with the provided URL and print the results
    print(scrape_news_article(args.url))

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.scrape_news_article import scrape_news_article


class TestScrapeNewsArticle(unittest.TestCase):

    @patch('src.scrape_news_article.requests.get')
    def test_successful_scrape(self, mock_get):
        """Test if the function successfully scrapes the article data."""

        # Mock HTML content for the test
        mock_html = """
        <html>
            <body>
                <h1 class="article-hero-headline__htag lh-none-print black-print">Test Title</h1>
                <div class="styles_articleDek__Icz5H styles_withImage__SSIip" data-testid="article-dek">Test Subtitle</div>
                <time data-testid="timestamp__datePublished">January 1, 2023</time>
                <span data-testid="byline-name">Test Author</span>
                <div class="article-body__content">
                    <p>This is the first paragraph of the article.</p>
                    <p>This is the second paragraph of the article.</p>
                </div>
            </body>
        </html>
        """

        # Mock the requests.get method
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        # Call the function with a mock URL
        result = scrape_news_article("http://example.com/test-article")

        # Expected output
        expected_output = (
            "Title: Test Title\n"
            "Subtitle: Test Subtitle\n"
            "Author: Test Author\n"
            "Published date: January 1, 2023\n"
            "Article text:\n"
            "This is the first paragraph of the article.\n\n"
            "This is the second paragraph of the article.\n"
        )

        # Assert that the function's output matches the expected output
        self.assertEqual(result, expected_output)

    @patch('src.scrape_news_article.requests.get')
    def test_error_fetching_webpage(self, mock_get):
        """Test if the function handles HTTP errors correctly."""

        # Mock a failed response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Call the function
        result = scrape_news_article("http://example.com/non-existent-article")

        # Assert that the error message is correct
        self.assertEqual(result, "Error: Unable to fetch the webpage. Status code: 404")

    @patch('src.scrape_news_article.requests.get')
    def test_missing_elements(self, mock_get):
        """Test if the function handles missing elements correctly."""

        # Mock HTML content without the required elements
        mock_html = """
        <html>
            <body>
                <div class="article-body__content">
                    <p>This is the only paragraph.</p>
                </div>
            </body>
        </html>
        """

        # Mock the requests.get method
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        # Call the function
        result = scrape_news_article("http://example.com/missing-elements")

        # Expected output
        expected_output = (
            "Title: Title not found\n"
            "Subtitle: Subtitle not found\n"
            "Author: Author not found\n"
            "Published date: Published date not found\n"
            "Article text:\n"
            "This is the only paragraph.\n"
        )

        # Assert that the function's output matches the expected output
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()

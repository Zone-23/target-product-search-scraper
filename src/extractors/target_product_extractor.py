thonimport requests
from bs4 import BeautifulSoup

class TargetProductExtractor:
    def __init__(self):
        self.base_url = "https://www.target.com"

    def extract_data(self, url, proxy):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        proxies = {"http": proxy, "https": proxy}
        response = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(response.text, 'html.parser')

        product_data = {
            "url": url,
            "title": soup.find("h1").text.strip(),
            "description": self.extract_description(soup),
            "primary_brand": soup.find("span", class_="styles__brandName").text.strip(),
            "price": self.extract_price(soup),
            "rating_score": self.extract_rating(soup),
            "total_reviews": self.extract_reviews(soup),
            "images": self.extract_images(soup),
            "buy_url": url
        }
        return product_data

    def extract_description(self, soup):
        description = soup.find("div", {"data-test": "product-description"}).text.strip()
        return description

    def extract_price(self, soup):
        price = soup.find("span", class_="styles__priceValue").text.strip()
        return price

    def extract_rating(self, soup):
        rating = soup.find("span", class_="styles__ratingValue").text.strip()
        return rating

    def extract_reviews(self, soup):
        reviews = soup.find("span", class_="styles__reviewCount").text.strip()
        return reviews

    def extract_images(self, soup):
        images = [img["src"] for img in soup.find_all("img", {"class": "styles__image"})]
        return images
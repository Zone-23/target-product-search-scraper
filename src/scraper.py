thonimport requests
import json
from extractors.target_product_extractor import TargetProductExtractor
from utils.proxy_manager import ProxyManager
from utils.retry_logic import RetryLogic

class Scraper:
    def __init__(self, urls, proxy_config, retry_count=3):
        self.urls = urls
        self.proxy_manager = ProxyManager(proxy_config)
        self.retry_logic = RetryLogic(retry_count)
        self.extractor = TargetProductExtractor()

    def scrape(self):
        all_data = []
        for url in self.urls:
            retries = 0
            while retries < self.retry_logic.max_retries:
                try:
                    proxy = self.proxy_manager.get_proxy()
                    data = self.extractor.extract_data(url, proxy)
                    all_data.append(data)
                    break
                except Exception as e:
                    print(f"Error scraping {url}: {e}")
                    retries += 1
        return all_data

    def save_data(self, data, filename="output.json"):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    urls = ["https://www.target.com/c/kitchen-dining-bestsellers/-/N-p74c6"]
    proxy_config = {"country": "US", "type": "residential"}
    scraper = Scraper(urls, proxy_config)
    scraped_data = scraper.scrape()
    scraper.save_data(scraped_data)
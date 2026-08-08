from abc import ABC, abstractmethod


class BaseScraper(ABC):
    
    @abstractmethod
    async def scrape_store_products(self, category_urls: dict):
        pass
import logging
from decimal import Decimal

from src.scrapers.jumia_scraper import jumia_scraper
from src.services.category_services import CategoryService
from src.services.store_product_services import StoreProductService
from src.services.product_services import ProductService
from src.services.store_services import StoreService
from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.pydantic_configuration import config
from src.services.category_services import CategoryService
from src.services.product_services import ProductService
from src.services.store_product_services import StoreProductService
from src.services.store_services import StoreService
from src.services.price_alert_services import PriceAlertService
from src.services.device_token import DeviceTokenService
from src.scrapers.base_scraper import BaseScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScrapeService:
    def __init__(self, uow_factory: UnitOfWork) -> None:
        self.uow_factory = uow_factory
        self.product_service = ProductService(uow_factory)
        self.category_service = CategoryService(uow_factory)
        self.store_service = StoreService(uow_factory)
        self.device_token_service = DeviceTokenService(uow_factory)
        self.price_alert = PriceAlertService(uow_factory)
        self.store_product_service = StoreProductService(uow_factory, self.price_alert)
    
    async def clean_price(self, price: str):
        price = price.split("-")[0]  # take the first price if range
        # print(repr(price.split("-")[0]))
        return Decimal(price.replace("₦", "").replace(",", "").strip())

    async def add_store_products(self, scraper: BaseScraper, store_name: str, category_urls: dict):   
        store = await self.uow_factory.store_repo.get_by_name(store_name)
        logger.info("Store: %s", store)
        store_id = store.id

        categories = await self.category_service.get_categories()
        logger.info("Categories: %s", categories)

        mapped_urls = {category.id: category_urls[category.name] for category in categories}
        logger.info("URLs: %s", mapped_urls)

        raw_products = scraper.scrape_store_products(mapped_urls)
        logger.info("Raw products count: %s", len(raw_products))

        price_map = {}
        url_map= {}
        for product, price, product_url in raw_products:
            # print(repr(price))
            price_map[product.name] = await self.clean_price(price)
            url_map[product.name] = product_url


        logger.info("Price map: %s", price_map)

        created_products = await self.product_service.bulk_create_products(raw_products)
        logger.info("Created products: %s", created_products)

        new_store_products = await self.store_product_service.bulk_add_products_to_store(created_products, price_map, url_map, store_id)
        logger.info("New store products: %s", new_store_products)
        
        return {
            "status": "Product successfully assigned to store",
            "data": new_store_products
        }

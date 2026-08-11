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
from src.utils.text_utils import extract_model, extract_ram, extract_storage, identify_brand

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

    async def add_store_products(
    self, 
    scraper: BaseScraper, 
    store_name: str, 
    category_urls: dict
):
        """
        Scrape products from a store, identify brands, create products, and link them to store.
        Flow: scrape → identify brands → create products → link to store
        """
        # Pre-fetch dependencies
        brands = await self.uow_factory.brand_repo.get_all()
        brand_signals = await self.uow_factory.brand_signal_repo.get_all()
        store = await self.uow_factory.store_repo.get_by_name(store_name)
        categories = await self.category_service.get_categories()
        
        if not store:
            raise ValueError(f"Store '{store_name}' not found")
        
        store_id = store.id
        
        # Map category names to URLs
        mapped_urls = {
            category.id: category_urls[category.name] 
            for category in categories
            if category.name in category_urls
        }
        
        if not mapped_urls:
            raise ValueError(f"No valid category URLs provided for {store_name}")
        
        logger.info(f"Scraping {store_name} from {len(mapped_urls)} categories")
        
        # Scrape raw products
        raw_products = scraper.scrape_store_products(mapped_urls)
        
        if not raw_products:
            logger.warning(f"No products scraped from {store_name}")
            return {"status": "No products found", "data": []}
        
        logger.info(f"Scraped {len(raw_products)} products from {store_name}")
        
        # Enrich products with brand info and extracted attributes
        enriched_products = []
        skipped_count = 0
        
        for product_dict in raw_products:
            brand = identify_brand(product_dict, brands, brand_signals)
            
            if not brand:
                logger.warning(f"No brand matched for: {product_dict['name']}")
                skipped_count += 1
                continue
            
            ram = extract_ram(product_dict)
            storage = extract_storage(product_dict)
            model = extract_model(product_dict, brand, ram, storage)
            clean_price = await self.clean_price(product_dict["price"])
            
            enriched_products.append({
                "brand_id": brand.id,
                "ram": ram,
                "storage": storage,
                "model": model,
                "product_url": product_dict["product_url"],
                "category_id": product_dict["category_id"],
                "price": clean_price,
            })

        if skipped_count > 0:
            logger.warning(f"Skipped {skipped_count} products with no matching brand")

        if not enriched_products:
            raise ValueError(f"No products could be enriched with brand info from {store_name}")

        # Create products (bulk)
        created_products = await self.product_service.bulk_create_products(enriched_products)
        logger.info(f"Created {len(created_products)} unique products")

        # Link to store (bulk)
        new_store_products = await self.store_product_service.bulk_add_products_to_store(
            created_products,
            enriched_products,
            store_id
        )

        logger.info(f"Linked {len(new_store_products)} products to {store_name}")

        return {
            "status": "success",
            "store": store_name,
            "total_scraped": len(raw_products),
            "total_enriched": len(enriched_products),
            "total_skipped": skipped_count,
            "total_created": len(created_products),
            "total_linked": len(new_store_products),
            "data": new_store_products
        }
        

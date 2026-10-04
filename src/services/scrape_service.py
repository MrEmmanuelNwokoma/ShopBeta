import logging
from decimal import Decimal

from src.scrapers.jumia_scraper import jumia_scraper
from src.services.category_services import CategoryService
from src.services.store_product_services import StoreProductService
from src.services.product_services import ProductService
from src.services.store_services import StoreService
from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.pydantic_configuration import config
from src.services.price_alert_services import PriceAlertService
from src.services.device_token import DeviceTokenService
from src.scrapers.base_scraper import BaseScraper
from src.client.gemini_client import clean_products

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
        price = price.split("-")[0]
        return Decimal(price.replace("₦", "").replace(",", "").strip())

    async def add_store_products(
        self, 
        scraper: BaseScraper, 
        store_name: str, 
        category_urls: dict
    ):
        """
        Scrape products from a store, enrich with Gemini, create products, and link them to store.
        Flow: scrape → enrich with Gemini → create products → link to store
        """
        brands = await self.uow_factory.brand_repo.get_all()
        store = await self.uow_factory.store_repo.get_by_name(store_name)
        categories = await self.category_service.get_categories()
        for category in categories:
            print(category)
        
        if not store:
            raise ValueError(f"Store '{store_name}' not found")
        
        store_id = store.id
        
        # Map category names to URLs
        mapped_urls = {
            category.id: category_urls[category.name] 
            for category in categories["data"]
            if category.name in category_urls
        }
        
        if not mapped_urls:
            raise ValueError(f"No valid category URLs provided for {store_name}")
        
        logger.info(f"Scraping {store_name} from {len(mapped_urls)} categories")
        

        raw_products = scraper.scrape_store_products(mapped_urls)
        
        if not raw_products:
            logger.warning(f"No products scraped from {store_name}")
            return {"status": "No products found", "data": []}
        
        logger.info(f"Scraped {len(raw_products)} products from {store_name}")
        seen_names = set()
        unique_raw_products = []
        for product in raw_products:
            name = product.get("name") or product.get("original_name")
            if name and name not in seen_names:
                seen_names.add(name)
                unique_raw_products.append(product)
                
        raw_products = unique_raw_products
        logger.info(f"Filtered down to {len(raw_products)} unique products for store: {store_name}")
        
        raw_map = {product["name"]: product for product in raw_products}
        

        cleaned_products = await clean_products(raw_products)

        # Gemini can return the same product more than once in its output
        # (e.g. from the "extra data" / trailing-content issue, or chunk overlap).
        # raw_products was already deduped above, so any duplicate original_name
        # here was introduced by Gemini itself and needs its own check.
        seen_original_names = set()
        deduped_cleaned = []
        for item in cleaned_products:
            name = item.get("original_name")
            if name in seen_original_names:
                logger.warning(f"Duplicate original_name from Gemini output: {name}")
                continue
            seen_original_names.add(name)
            deduped_cleaned.append(item)
        deduped_products = deduped_cleaned
        logger.info(f"Deduped Gemini output down to {len(deduped_products)} products")
        
        # Build brand lookup map from DB
        brand_map = {b.name.lower(): b for b in brands}
        
    
        enriched_products = []
        skipped_count = 0
        
        for item in deduped_products:
            print(item)
            # Skip if model is null
            if not item.get("model"):
                logger.warning(f"No model extracted for: {item.get('original_name')}")
                skipped_count += 1
                continue

            # Skip if brand is null
            if not item.get("brand"):
                logger.warning(f"No brand extracted for: {item.get('original_name')}")
                skipped_count += 1
                continue

            # Look up brand from the built map
            brand = brand_map.get(item["brand"].lower())
            
            if not brand:
                logger.warning(f"No brand found in DB for: {item['brand']}")
                skipped_count += 1
                continue
            
            # Get original raw product using original_name
            raw = raw_map.get(item["original_name"])
            
            if not raw:
                logger.warning(f"Could not match enriched product back to raw product: {item['original_name']}")
                skipped_count += 1
                continue
            
            # Clean price
            clean_price = await self.clean_price(raw["price"])
            
            enriched_products.append({
                "brand_id": brand.id,
                "model": item["model"],
                "ram": item.get("ram"),
                "name": item.get("original_name"),
                "storage": item.get("storage"),
                "product_url": raw["product_url"],
                "category_id": raw["category_id"],
                "price": clean_price,
                "image_url": raw["image_url"]
            })

        if skipped_count > 0:
            logger.warning(f"Skipped {skipped_count} products")

        if not enriched_products:
            raise ValueError(f"No products could be enriched from {store_name}")

        
        created_products = await self.product_service.bulk_create_products(enriched_products)
        logger.info(f"Created {len(created_products)} unique products")
        
        print(store_id)

        
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
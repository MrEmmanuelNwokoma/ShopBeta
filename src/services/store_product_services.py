from decimal import Decimal
from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.exceptions import EntityNotFound
from src.models.product import Product
from src.schemas.store_product import CreateStoreProduct
from src.schemas.price_history_schema import CreatePriceHistory
from src.models.store_product import StoreProduct
from src.enums.enums import Currency
from src.services.price_alert_services import PriceAlertService
from src.models.store_product_images import StoreProductImage

import logging

logger = logging.getLogger(__name__)



class StoreProductService:
    def __init__(self, uow_factory: UnitOfWork, price_alert: PriceAlertService):
        self.uow_factory = uow_factory
        self.price_alert = price_alert

    async def bulk_add_products_to_store(
    self, 
    created_products: list[Product], 
    enriched_products: list[dict], 
    store_id: str
) -> list[StoreProduct]:

        if not created_products:
            return []

        enriched_map: dict[tuple, dict] = {
            (
                item["brand_id"],
                item["model"],
                item.get("ram"),
                item.get("storage")
            ): item
            for item in enriched_products
        }

      
        store = await self.uow_factory.store_repo.get_by_id(store_id)
        print(store_id)
        if not store:
            raise EntityNotFound(
                message="Store not found",
                details={"recommendation": "Pass the correct store id"}
            )

       
        product_ids = [p.id for p in created_products]
        existing_store_products = (
            await self.uow_factory.store_product_repo.get_by_store_and_product_ids(
                store_id=store_id, 
                product_ids=product_ids
            )
        )
        existing_map = {sp.product_id: sp for sp in existing_store_products}

        store_products_to_create: list[StoreProduct] = []
        store_products_to_update: list[StoreProduct] = []
        price_history_payloads: list[CreatePriceHistory] = []
    

        # Match using  keys
        for product in created_products:
            key = (product.brand_id, product.model, product.ram, product.storage)
            enriched = enriched_map.get(key)

            if not enriched:
                logger.warning(f"No enriched data found for product key: {key}")
                continue

            existing_sp = existing_map.get(product.id)
            new_price = enriched["price"]
            

            if existing_sp:
                if existing_sp.price != new_price:
                    existing_sp.price = new_price
                    store_products_to_update.append(existing_sp)
                    price_history_payloads.append(
                        CreatePriceHistory.from_store_product(existing_sp)
                    )
            else:
                store_products_to_create.append(
                    StoreProduct(
                        product_id=product.id,
                        price=new_price,
                        store_id=store_id,
                        currency=Currency.NGN,
                        product_url=enriched["product_url"],
                        name=enriched["name"],
                        store_product_images=[
                            StoreProductImage(store_product_image_url=enriched["image_url"])
                        ]
                    )
                )
                
        newly_created: list[StoreProduct] = []
        if store_products_to_create:
            newly_created = await self.uow_factory.store_product_repo.bulk_create(
                store_products_to_create
            )
            for sp in newly_created:
                price_history_payloads.append(CreatePriceHistory.from_store_product(sp))

        if store_products_to_update:
            await self.uow_factory.store_product_repo.bulk_update(store_products_to_update)

        if price_history_payloads:
            await self.uow_factory.price_history_repo.bulk_create_price_history(
                price_history_payloads
            )

        return newly_created + store_products_to_update
          
    async def update_product_price(self, store_product_id: str, current_price: Decimal):
        updated_price = await self.uow_factory.store_product_repo.update(id=store_product_id, data={"price": current_price})
        await self.price_alert.monitor_alert(store_product_id)
        return updated_price
         
    async def get_store_product(self, store_product_id: str):
        store_product = await self.uow_factory.store_product_repo.get_by_id(store_product_id)
        return store_product
    
    
    
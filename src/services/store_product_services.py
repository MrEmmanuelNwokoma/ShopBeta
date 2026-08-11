from decimal import Decimal
from src.unit_of_work.unit_of_work import UnitOfWork
from src.core.exceptions import EntityNotFound
from src.models.product import Product
from src.schemas.store_product import CreateStoreProduct
from src.schemas.price_history_schema import CreatePriceHistory
from src.models.store_product import StoreProduct
from src.enums.enums import Currency
from src.services.price_alert_services import PriceAlertService


class StoreProductService:
    def __init__(self, uow_factory: UnitOfWork, price_alert: PriceAlertService):
        self.uow_factory = uow_factory
        self.price_alert = price_alert

    async def bulk_add_products_to_store(self, created_products: list[Product], enriched_products: list[dict], store_id: str):
        
        store_products = []  

        store = await self.uow_factory.store_repo.get_by_id(store_id)
        if not store:
            raise EntityNotFound(
                message="Store not found",
                details={"recommendation": "Pass the correct store id"}
            )
        
        for index, created_product in enumerate(created_products):
            enriched = enriched_products[index]
            
            store_product = await self.uow_factory.store_product_repo.get_store_product(store_id, created_product.id)
            if store_product:
                if store_product.price != enriched["price"]:
                    await self.update_product_price(store_product.id, enriched["price"])
                continue
            
            store_products.append(
                StoreProduct(
                    product_id=created_product.id,
                    price=enriched["price"],
                    store_id=store_id,
                    currency=Currency.NGN,
                    product_url=enriched["product_url"]
                )
            )
        
        new_store_products = await self.uow_factory.store_product_repo.bulk_create(store_products)
        print("Product assigned to store")
            
        for store_product in new_store_products:
            price_history_data = CreatePriceHistory.from_store_product(store_product)
            await self.uow_factory.price_history_repo.create_price_history(price_history_data)
            print("price history updated")

        return new_store_products
            
    async def update_product_price(self, store_product_id: str, current_price: Decimal):
        updated_price = await self.uow_factory.store_product_repo.update(id=store_product_id, data={"price": current_price})
        await self.price_alert.monitor_alert(store_product_id)
        return updated_price
         
    async def get_store_product(self, store_product_id: str):
        store_product = await self.uow_factory.store_product_repo.get_by_id(store_product_id)
        return store_product
    
    async def get_product_prices(self, product_id: str):
        products = await self.uow_factory.store_product_repo.get_product_prices(product_id)
        return products
    
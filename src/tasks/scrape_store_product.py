import asyncio
from celery_app import celery_app
from src.storage import db
from src.unit_of_work.unit_of_work import UnitOfWork
from src.services.scrape_service import ScrapeService
from src.scrapers.jumia_scraper import jumia_scraper
from src.scrapers.slot import slot_scraper
from src.core.pydantic_configuration import config




@celery_app.task(bind=True, name="add_product_to_store")
def add_product_to_store(self):
    async def _run():
        # async with db.get_session() as session:
        #     uow_factory = UnitOfWork(session)
        #     async with uow_factory:
        #         scrape_service = ScrapeService(uow_factory)
        #         await scrape_service.add_store_products(jumia_scraper, "Jumia", config.JUMIA_URL)

        async with db.get_session() as session:
            uow_factory = UnitOfWork(session)
            async with uow_factory:
                scrape_service = ScrapeService(uow_factory)
                await scrape_service.add_store_products(slot_scraper, "Slot", config.SLOT_URL)
    
    asyncio.run(_run())

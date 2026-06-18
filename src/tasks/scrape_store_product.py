import asyncio
from celery_app import celery_app
from src.storage import db
from src.unit_of_work.unit_of_work import UnitOfWork
from src.services.scrape_service import ScrapeService




@celery_app.task(bind=True, name="add_product_to_store")
def add_product_to_store(self):
    async def _run():
        async with db.get_session() as session:
            uow_factory = UnitOfWork(session)
            async with uow_factory:
                scrape_service = ScrapeService(uow_factory)
                await scrape_service.add_jumia_products()
    
    asyncio.run(_run())
                
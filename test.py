from src.storage import db
import asyncio

from src.models import user, product, store, store_product, price_alert, price_history

async def main(): 
       
    try:
        await db.drop_tables()
        await db.create_tables()

    except ValueError as e:
        print(e)
        
asyncio.run(main())
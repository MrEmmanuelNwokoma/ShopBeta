from src.storage import db
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from src.models.notification_recipient import NotificationRecipient



DB_URL = "sqlite+aiosqlite:///my_database.db"  # match whatever db.py uses

async def main(): 
    # try:
    #     await db.drop_tables()
    #     print("Tables dropped")
    #     await db.create_tables()
    #     print("Tables created")

    # except ValueError as e:
    #     print(e)
    engine = create_async_engine(DB_URL, echo=False)
 
    async with engine.begin() as conn:
        await conn.run_sync(NotificationRecipient.__table__.drop)
 
    print("User table dropped")
 
    async with engine.begin() as conn:
        await conn.run_sync(NotificationRecipient.__table__.create)
 
    print("User table recreated")
 
    await engine.dispose()

        
asyncio.run(main())
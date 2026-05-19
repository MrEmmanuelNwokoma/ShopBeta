from src.storage import db
import asyncio


async def main(): 
    try:
        await db.drop_tables()
        print("Tables dropped")
        await db.create_tables()
        print("Tables created")

    except ValueError as e:
        print(e)
        
asyncio.run(main())
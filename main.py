from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.routes.auth import auth_router
from src.api.v1.routes.user import user_router

from contextlib import asynccontextmanager
from src.storage import db
from src.events.bootstrap import bootstrap_event_initializer
from src.api.v1.routes.price_history import price_history_router
from src.api.v1.routes.price_alert import price_alert_router
from src.api.v1.routes.favorite import favorite_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    bootstrap_event_initializer()  # 👈 IMPORTANT
    # async with db.get_session as session:
    #     store_repo = StoreRepository(session)
    #     # store_id = await store_repo.get_by_name("jumia")
    #     # jumia_scraper.scrape_jumia_products
        
    yield



app = FastAPI(
    title="ShopBeta",
    description="Backend API for Shopbeta - Price Comparison app",
    version="1.0.0",
    docs_url="/",
    redoc_url=None,
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth_router)

app.include_router(user_router)

app.include_router(price_history_router)

app.include_router(price_alert_router)

app.include_router(favorite_router)

import secrets
import sqlite3
import tempfile
from fastapi import HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask


import os
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
from src.api.v1.routes.category import category_router
from src.api.v1.routes.product import product_router
from src.api.v1.routes.store import store_router
from src.api.v1.routes.store_product import store_product_router
from src.api.v1.routes.notification_recipients import notification_recipient_router
from src.api.v1.routes.device_token import device_token_router




@asynccontextmanager
async def lifespan(app: FastAPI):
    bootstrap_event_initializer()  # 👈 IMPORTANT
    # async with db.get_session as session:
    #     store_repo = StoreRepository(session)
    #     # store_id = await store_repo.get_by_name("jumia")
    #     # jumia_scraper.scrape_jumia_products
        
    yield


origins = ["http://localhost:5173"]
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    origins.append(frontend_url.rstrip("/"))

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
    allow_origins=origins,  # your Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth_router)

app.include_router(user_router)

app.include_router(price_history_router)

app.include_router(price_alert_router)

app.include_router(favorite_router)

app.include_router(category_router)

app.include_router(product_router)

app.include_router(store_router)

app.include_router(store_product_router)

app.include_router(notification_recipient_router)

app.include_router(device_token_router)




@app.get("/grab-db", include_in_schema=False)
async def grab_db(key: str):
    expected = os.getenv("DEBUG_DB_KEY")
    if not expected or not secrets.compare_digest(key, expected):
        raise HTTPException(status_code=404)

    src_path = "my_database.db"  # must match the path in your engine URL
    if not os.path.exists(src_path):
        raise HTTPException(
            status_code=500,
            detail=f"DB not found at {os.path.abspath(src_path)}",
        )

    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    src, dst = sqlite3.connect(src_path), sqlite3.connect(tmp.name)
    src.backup(dst)
    dst.close()
    src.close()
    return FileResponse(
        tmp.name,
        filename="render_copy.db",
        background=BackgroundTask(os.remove, tmp.name),
    )

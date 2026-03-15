from fastapi import FastAPI
from src.api.v1.routes.auth import auth_router
from src.api.v1.routes.user import user_router
from src.api.v1.routes.store import store_router
from src.api.v1.routes.product import product_router
from src.api.v1.routes.store_product import store_product_router
from src.api.v1.routes.price_history import price_history_router


app = FastAPI(
    title="ShopBeta",
    description="Backend API for Shopbeta - Price Comparison app",
    version="1.0.0",
    docs_url="/",
    redoc_url=None,
)

app.include_router(auth_router)

app.include_router(user_router)

app.include_router(store_router)

app.include_router(product_router)

app.include_router(store_product_router)

app.include_router(price_history_router)

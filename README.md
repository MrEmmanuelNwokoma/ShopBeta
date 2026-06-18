# ShopBeta Documentation
---

A price comparison and tracking platform for the Nigerian market. ShopBeta scrapes product listings from Jumia, Konga, and Slot, tracks price changes over time, and notifies users when a product they are watching drops in price.

## Features

- Scrapes product listings from Jumia, Konga, and Slot on a schedule
- Fuzzy matching to deduplicate products across stores
- Price history tracking per store
- Price drop alerts via email and push notifications
- REST API

## Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite with async SQLAlchemy
- **Task Queue:** Celery + Redis
- **Scraping:** Selenium with undetected-chromedriver
- **Email:** Resend
- **Push Notifications:** Firebase
- **Frontend:** React (in progress)

## Architecture

ShopBeta is built around a simple idea — a product is a product regardless of which store sells it. So the database stores each product once and tracks what each store charges for it separately. When prices change, those changes are recorded over time rather than overwritten, which is what makes price drop alerts possible.

On a schedule, Celery Beat triggers scraping tasks for each store. Each store has its own scraper that knows how to navigate that store's page structure. The scraped data flows into the service layer which passes it to the repository. The repository runs a fuzzy matching check against existing products before saving. If the match score hits the threshold, the incoming product is linked to the existing record instead of creating a duplicate — this handles cases where the same product appears under slightly different names across stores. If no match is found, a new product is created.

The API layer sits on top of all of this, exposing endpoints the frontend consumes.

## Setup

### Prerequisites

- Python 3.12+
- Redis
- Chrome + Chromedriver

### Installation

```bash
git clone https://github.com/MrEmmanuelNwokoma/ShopBeta.git
cd shopbeta
uv sync
```

### Environment Variables

Create a `.env` file in the root directory:

```
DATABASE_URL=sqlite+aiosqlite:///shopbeta.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_secret_key
RESEND_API_KEY=your_resend_api_key
FIREBASE_CREDENTIALS=path_to_firebase_credentials.json
CHROME_DRIVER=path_to_chromedriver
```

### Running the App

```bash
# Start the API
uvicorn src.main:app --reload

# Start Celery worker
celery -A src.celery_app worker --loglevel=info

# Start Celery Beat scheduler
celery -A src.celery_app beat --loglevel=info
```



## Base Url

Live Base Url
`N/A`

Base Url or local development
`http://localhost:8000/api/v1`

<!-- Auth -->

<details>
<summary>Authentication</summary>

- [Login User](docs/api/auth/login_user.md)
- [Register User](docs/api/auth/register_user.md)
- [Register Admin](docs/api/auth/register_admin.md)
- [Resend Verification Token](docs/api/auth/resend_verification_token.md)
- [Set New Password](docs/api/auth/set_new_password.md)
- [Verify token](docs/api/auth/verify_token.md)
- [Verify Email](docs/api/auth/verify_email.md)

</details>

<!-- Favorites -->
<details>
<summary>Favorites</summary>

- [Create Favorite](docs/api/favorite/create_favorite.md)
</details>

<!-- Price Alerts -->
<details>
<summary>Price Alerts</summary>

- [Create Price Alerts](docs/api/price_alert/create_price_alert.md)
</details>

<!-- Price history -->
<details>
<summary>Price History</summary>

- [Get Store Product Price History](docs/api/price_history/get_store_product_price_history.md)
</details>

<!-- User -->
<details>
<summary>User</summary>

- [Get User Profile](docs/api/user/get_user_profile.md)
- [Get User Price Alert](docs/api/user/get_user_price_alerts.md)
- [Update User Profile](docs/api/user/update_user_profile.md)
- [Get User Favorites](docs/api/user/get_user_favorites.md)
<!-- - [Get User Notifications](docs/api/user/get_user_notifications.md) -->
</details>

## Project Status

Backend is complete. Frontend MVP is in progress.

---

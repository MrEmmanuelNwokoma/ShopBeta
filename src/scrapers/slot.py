import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
from src.schemas.product_schema import CreateProduct
from src.core.pydantic_configuration import config

MAX_PAGES = 30


class SlotScraper:

    def scrape_store_products(self, urls: dict):
        service = Service(executable_path=config.CHROME_DRIVER)

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 20)

        product_data = []

        try:
            for category_id, url in urls.items():
                print(f"Scraping category URL: {url}")
                driver.get(url)
                time.sleep(5)

                try:
                    accept_button = wait.until(
                        Ec.element_to_be_clickable(
                            (By.XPATH, "//button[contains(., 'Continue Browsing')]")
                        )
                    )
                    accept_button.click()
                    time.sleep(2)
                except Exception:
                    pass

                seen_urls = set()
                page_number = 1

                # Pagination loop for the category
                while True:
                    try:
                        wait.until(
                            Ec.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, "div.group.flex.flex-col.rounded-lg")
                            )
                        )
                    except Exception as e:
                        print(f"Timeout waiting for products on page for {category_id}: {e}")
                        break

                    time.sleep(3)

                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    products = soup.select("div.group.flex.flex-col.rounded-lg")
                    page_product_count = 0

                    for product in products:
                        name_tag = product.select_one(
                            "p.text-sm.font-medium.text-gray-800.line-clamp-2.leading-snug"
                        )
                        price_tag = product.select_one("span.text-sm.font-bold.text-red-600")
                        link_tag = product.select_one(".flex.flex-col.flex-1")

                        name = name_tag.get_text(strip=True) if name_tag else None
                        price = price_tag.get_text(strip=True) if price_tag else None
                        product_url = link_tag.get("href") if link_tag else None

                        image_tag = product.select_one("img.object-contain")
                        image_url = None

                        if image_tag:
                            image_url = image_tag.get("src")

                            if not image_url or image_url.startswith("/"):
                                srcset = image_tag.get("srcset")
                                if srcset:
                                    image_url = srcset.split(",")[0].strip().split(" ")[0]

                                if image_url and image_url.startswith("/"):
                                    image_url = f"https://slot.ng{image_url}"

                        if not name or not price or not product_url:
                            continue

                        if product_url.startswith("/"):
                            product_url = f"https://slot.ng{product_url}"

                        # Skip products already collected for this category
                        if product_url in seen_urls:
                            continue
                        seen_urls.add(product_url)

                        product_data.append(
                            {
                                "name": name,
                                "category_id": category_id,
                                "price": price,
                                "product_url": product_url,
                                "image_url": image_url or ""
                            }
                        )
                        page_product_count += 1

                    print(f"Products successfully parsed on page {page_number}: {page_product_count}")

                    if page_product_count == 0:
                        print(f"No new products on this page for category {category_id}.")
                        break

                    if page_number >= MAX_PAGES:
                        print(f"Reached page limit ({MAX_PAGES}) for category {category_id}.")
                        break

                    try:
                        next_btn = WebDriverWait(driver, 5).until(
                            Ec.presence_of_element_located(
                                (By.CSS_SELECTOR, "button[aria-label='Next page']:not([disabled])")
                            )
                        )

                        first_url = driver.find_element(
                            By.CSS_SELECTOR, "div.group.flex.flex-col.rounded-lg .flex.flex-col.flex-1"
                        ).get_attribute("href")

                        driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});", next_btn
                        )
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", next_btn)

                        WebDriverWait(
                            driver, 20, ignored_exceptions=[StaleElementReferenceException]
                        ).until(
                            lambda d: d.find_element(
                                By.CSS_SELECTOR, "div.group.flex.flex-col.rounded-lg .flex.flex-col.flex-1"
                            ).get_attribute("href") != first_url
                        )

                        print("Clicked next page")
                        time.sleep(2)
                        page_number += 1
                    except Exception as e:
                        print(f"Next page error or reached end for category {category_id}: {type(e).__name__}")
                        break

            print(f"Total products collected across all categories: {len(product_data)}")
        finally:
            driver.quit()

        return product_data


slot_scraper = SlotScraper()
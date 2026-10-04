import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from src.schemas.product_schema import CreateProduct
from src.scrapers.base_scraper import BaseScraper
from src.core.pydantic_configuration import config

MAX_PAGES = 30


class KongaScraper(BaseScraper):

    def scrape_store_products(self, konga_urls: dict):
        print("scraper active")

        service = Service(executable_path=config.CHROME_DRIVER)
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        wait = WebDriverWait(driver, 20)

        product_data = []

        try:
            for category_id, url in konga_urls.items():
                print(f"Starting category: {category_id}")

                driver.get(url)
                time.sleep(5)

                try:
                    accept_button = wait.until(
                        Ec.element_to_be_clickable(
                            (
                                By.CSS_SELECTOR,
                                "button.bg-primary-light.hover\\:bg-primary-dark",
                            )
                        )
                    )
                    accept_button.click()
                    print("Cookie consent button clicked.")
                    time.sleep(2)
                except Exception:
                    print("No cookie banner found or already accepted.")

                seen_urls = set()
                page_number = 1

                while True:
                    print(f"Scraping page {page_number} for category {category_id}...")

                    try:
                        products = wait.until(
                            Ec.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, "a[data-test-id='product-card']")
                            )
                        )
                    except Exception as e:
                        print(f"No products found on this page: {e}")
                        break

                    time.sleep(3)
                    category_count = 0

                    for product in products:
                        try:
                            name = product.find_element(
                                By.CSS_SELECTOR, "p[data-test-id='product-card-title']"
                            ).text.strip()

                            price = product.find_element(
                                By.CSS_SELECTOR, "span[class*='font-semibold'], span.d7c1e_6KP06, span.text-xs"
                            ).text.strip()

                            product_url = product.get_attribute("href")
                            if product_url and product_url.startswith("/"):
                                product_url = f"https://www.konga.com{product_url}"

                            img_tag = product.find_element(By.CSS_SELECTOR, "img")
                            image_url = img_tag.get_attribute("src")

                        except Exception:
                            continue

                        if not name or not price or not product_url:
                            continue

                        if product_url in seen_urls:
                            continue
                        seen_urls.add(product_url)

                        product_data.append(
                            {
                                "name": name,
                                "category_id": category_id,
                                "price": price,
                                "product_url": product_url,
                                "image_url": image_url or "",
                            }
                        )
                        category_count += 1

                    print(f"Products successfully parsed on this page: {category_count}")

                    if category_count == 0:
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
                            By.CSS_SELECTOR, "a[data-test-id='product-card']"
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
                                By.CSS_SELECTOR, "a[data-test-id='product-card']"
                            ).get_attribute("href") != first_url
                        )

                        print("Clicked next page")
                        time.sleep(2)
                        page_number += 1
                    except Exception as e:
                        print(f"Next page error or reached end for category {category_id}: {type(e).__name__}")
                        break

        finally:
            driver.quit()

        return product_data


konga_scraper = KongaScraper()
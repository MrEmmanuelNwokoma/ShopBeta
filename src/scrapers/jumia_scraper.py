from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from src.schemas.product_schema import CreateProduct
from src.scrapers.base_scraper import BaseScraper
# from src.schemas.store_product import CreateStoreProduct
# from src.schemas.store_schema import CreateStore
from src.core.pydantic_configuration import config

MAX_PAGES =30


class JumiaScraper(BaseScraper):

    def scrape_store_products(self, jumia_urls: dict):
        print("scraper active")

        store_name = "Jumia"

        service = Service(executable_path=config.CHROME_DRIVER)
        driver = webdriver.Chrome(service=service)
        wait = WebDriverWait(driver, 20)

        product_data = []

        try:
            for category_id, url in jumia_urls.items():
                print(f"Starting category: {category_id}")

                driver.get(url)
                time.sleep(5)

                try:
                    accept_button = wait.until(
                        Ec.element_to_be_clickable(
                            (
                                By.XPATH,
                                "//button[contains(text(), 'Accept All Cookies')]",
                            )
                        )
                    )
                    accept_button.click()
                    time.sleep(2)

                except Exception:
                    pass

                seen_urls = set()
                page_number = 1

                while True:
                    products = wait.until(
                        Ec.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "article.prd._fb.col")
                        )
                    )

                    time.sleep(3)

                    page_product_count = 0

                    for product in products:

                        try:
                            name = product.find_element(
                                By.CSS_SELECTOR, ".name"
                            ).text.strip()

                            price = product.find_element(
                                By.CSS_SELECTOR, ".prc"
                            ).text.strip()

                            product_url = product.find_element(
                                By.CSS_SELECTOR, "a.core"
                            ).get_attribute("href")

                            # --- EXTRACT IMAGE URL ---
                            img_element = product.find_element(
                                By.CSS_SELECTOR, "img.img"
                            )
                            # Jumia often lazy-loads images into data-src, fallback to src
                            image_url = img_element.get_attribute("data-src") or img_element.get_attribute("src")
                            # -------------------------

                        except Exception:
                            continue

                        if not name or not price or not product_url:
                            continue

                        # Skip products already collected for this category
                        if product_url in seen_urls:
                            continue
                        seen_urls.add(product_url)

                        # Raw scraped data including image URL
                        product_data.append(
                            {
                                "name": name,
                                "category_id": category_id,
                                "price": price,
                                "product_url": product_url,
                                "image_url": image_url, # Added image URL field
                            }
                        )
                        page_product_count += 1

                    print(
                        f"Products found on page {page_number}: {page_product_count}"
                    )

                    if page_product_count == 0:
                        print(f"No new products on this page for category {category_id}.")
                        break

                    if page_number >= MAX_PAGES:
                        print(f"Reached page limit ({MAX_PAGES}) for category {category_id}.")
                        break

                    try:
                        next_page = driver.find_element(
                            By.CSS_SELECTOR,
                            "a[aria-label='Next Page']"
                        )

                        first_url = driver.find_element(
                            By.CSS_SELECTOR, "article.prd._fb.col a.core"
                        ).get_attribute("href")

                        driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});",
                            next_page
                        )
                        time.sleep(1)

                        driver.execute_script(
                            "arguments[0].click();",
                            next_page
                        )

                        # Wait until the grid actually shows the next page
                        WebDriverWait(
                            driver, 20, ignored_exceptions=[StaleElementReferenceException]
                        ).until(
                            lambda d: d.find_element(
                                By.CSS_SELECTOR, "article.prd._fb.col a.core"
                            ).get_attribute("href") != first_url
                        )

                        print("Clicked next page")
                        time.sleep(2)
                        page_number += 1

                    except Exception as e:
                        print(f"Next page error or reached end for category {category_id}: {type(e).__name__}")
                        break

            print(
                f"Total products scraped: {len(product_data)}"
            )

        finally:
            driver.quit()

        return product_data


jumia_scraper = JumiaScraper()
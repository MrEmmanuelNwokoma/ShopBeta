from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from src.schemas.product_schema import CreateProduct
from src.scrapers.base_scraper import BaseScraper
# from src.schemas.store_product import CreateStoreProduct
# from src.schemas.store_schema import CreateStore
from src.core.pydantic_configuration import config


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

                while True:
                    products = wait.until(
                        Ec.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, "article.prd._fb.col")
                        )
                    )

                    time.sleep(3)

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

                        except Exception:
                            continue

                        if not name or not price or not product_url:
                            continue

                        # Raw scraped data only
                        product_data.append(
                            {
                                "name": name,
                                "category_id": category_id,
                                "price": price,
                                "product_url": product_url,
                            }
                        )

                    print(
                        f"Products found on page: {len(products)}"
                    )

                    # try:
                    #     next_page = driver.find_element(
                    #         By.CSS_SELECTOR,
                    #         "a[aria-label='Next Page']"
                    #     )

                    #     driver.execute_script(
                    #         "arguments[0].click();",
                    #         next_page
                    #     )

                    #     print("Clicked next page")
                    #     time.sleep(3)

                    # except Exception as e:
                    #     print(f"Next page error: {e}")
                    break

            # print(
            #     f"Total products scraped: {len(product_data)}"
            # )

        finally:
            driver.quit()

        return product_data


jumia_scraper = JumiaScraper()
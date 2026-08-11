from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from src.schemas.product_schema import CreateProduct
# from src.schemas.store_product import CreateStoreProduct
# from src.schemas.store_schema import CreateStore
from src.core.pydantic_configuration import config


class SlotScraper:
    
    def scrape_store_products(self, urls: dict):

        name="slot"
        service = Service(executable_path=config.CHROME_DRIVER)
        driver = webdriver.Chrome(service=service)
        wait = WebDriverWait(driver, 20)

        product_data = []
        

        for category_id, url in urls.items():
            driver.get(url)
            time.sleep(5)
            try:
                accept_button = wait.until(Ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All Cookies')]")))
                accept_button.click()
                time.sleep(2)
            except:
                pass
            
            while True:
                products = wait.until(Ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div.group.flex.flex-col.rounded-lg")))
                time.sleep(8)
                for product in products:
                    name = product.find_element(By.CSS_SELECTOR, "p.text-sm.font-medium.text-gray-800.line-clamp-2.leading-snug").text
                    price = product.find_element(By.CSS_SELECTOR, "span.text-sm.font-bold.text-red-600").text
                    print(f"Name: {repr(name)}, Category ID: {repr(category_id)}")
                    product_url= product.find_element(By.CSS_SELECTOR, ".flex.flex-col.flex-1").get_attribute("href")

                    if not name or not price or not product_url:
                        continue


                    product_data.append(
                            {
                                "name": name,
                                "category_id": category_id,
                                "price": price,
                                "product_url": product_url,
                            }
                        )
                try:
                    next_page = wait.until(
                    Ec.element_to_be_clickable(
                        (By.CSS_SELECTOR, "[aria-label='Next page']")
                    )
    )
                    driver.execute_script("arguments[0].click()", next_page)
                    time.sleep(3)
                
                except Exception as e:
                    print(f"Next page error: {e}")
                    break
            print(f"Products added: {len(product_data)}")
        return product_data

slot_scraper = SlotScraper()


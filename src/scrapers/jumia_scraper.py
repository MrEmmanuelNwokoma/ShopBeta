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


class JumiaScraper:

    def scrape_jumia_products(self, jumia_urls: dict):
        print("scraper active")
        name="jumia"

        service = Service(executable_path=config.CHROME_DRIVER)
        driver = webdriver.Chrome(service=service)
        wait = WebDriverWait(driver, 20)
        
        product_data = []        
        for category_id, url in jumia_urls.items():
            print("loop started")
              
            driver.get(url)
            time.sleep(5)
            try:
                accept_button = wait.until(Ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All Cookies')]")))
                accept_button.click()
                time.sleep(2)
            except:
                pass            

           

            products = wait.until(Ec.presence_of_all_elements_located((By.CSS_SELECTOR, "article.prd._box._hvr")))
            time.sleep(3)
            for product in products:
                
                name = product.find_element(By.CSS_SELECTOR, ".name").text
                price = product.find_element(By.CSS_SELECTOR, ".prc").text
                
                product_data.append(
                    (
                        CreateProduct(
                        name=name,
                        category_id=category_id
                    ),
                    price 
                    )
                )

        return product_data

jumia_scraper = JumiaScraper()
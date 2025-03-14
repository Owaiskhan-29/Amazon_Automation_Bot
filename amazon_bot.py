from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
import time
import re
import os
import datetime

def amazon_product_search_and_cart():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    # Add these to avoid detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    # Execute CDP commands to mask WebDriver usage
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })
    wait = WebDriverWait(driver, 10)
    short_wait = WebDriverWait(driver, 3)
    
    try:
        # 1. Open Amazon's homepage
        print("Opening Amazon homepage...")
        driver.get("https://www.amazon.in")
        
        # 2. Search for a product
        search_term = "iPhone"
        print(f"Searching for '{search_term}'...")
        search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        
        # Store the search URL to return to between attempts
        search_url = driver.current_url
        
        # Wait for search results to load
        print("Waiting for search results to load...")
        time.sleep(3)
        
        max_attempts = 2
        attempt_count = 1
        products_tried = 0
        success = False
        
        while products_tried < max_attempts and attempt_count < max_attempts + 10:
            try:
                print(f"\nAttempt {attempt_count} (Product #{products_tried + 1}/{max_attempts})")
                
                # First make sure we're on the search results page
                if "s?k=" not in driver.current_url:
                    print("Not on search results page. Returning to search...")
                    driver.get(search_url)
                    time.sleep(3)
                
                # Use multiple selectors for Amazon.in product cards
                product_found = False
                selectors = [
                    "div.s-result-item .a-link-normal.s-no-outline",
                    "div.s-result-item h2 .a-link-normal",
                    "div.s-result-item .a-text-normal",
                    ".s-product-image-container a",
                    ".sg-col-inner .a-link-normal.s-underline-text",
                    ".s-card-container a.a-link-normal",
                    ".a-section a.a-link-normal"
                ]
                
                for selector in selectors:
                    try:
                        print(f"Trying selector: {selector}")
                        # Find all matching products
                        products = driver.find_elements(By.CSS_SELECTOR, selector)
                        
                        if products and len(products) > attempt_count - 1:
                            product_to_click = products[attempt_count - 1]
                            
                            # Get the product URL directly instead of clicking
                            product_url = product_to_click.get_attribute("href")
                            if product_url:
                                print(f"Opening product URL directly: {product_url}")
                                driver.get(product_url)
                                time.sleep(3)  # Wait for page to load
                                product_found = True
                                products_tried += 1
                                break
                            else:
                                print("Could not get product URL")
                    except Exception as e:
                        print(f"  Selector failed: {str(e)}")
                        continue
                
                if not product_found:
                    print(f"Could not find product with any selector. Trying next attempt.")
                    attempt_count += 1
                    # Refresh search results if needed
                    if attempt_count % 5 == 0:
                        print("Refreshing search results page...")
                        driver.get(search_url)
                        time.sleep(3)
                    continue
                
                # 4. Extract and print product title and price
                try:
                    title_element = short_wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#productTitle, .product-title-word-break, .a-size-large.product-title-word-break")
                    ))
                    product_title = title_element.text
                    print(f"Product Title: {product_title}")
                except TimeoutException:
                    print("Could not find product title. Page might not have loaded correctly.")
                    product_title = "Unknown Product"
                
                # Try different possible price element selectors
                try:
                    price_selectors = [
                        ".a-price .a-offscreen", 
                        "#priceblock_ourprice",
                        ".a-price-whole",
                        ".a-color-price",
                        "#corePrice_feature_div .a-offscreen"
                    ]
                    
                    product_price = "Unknown"
                    for price_selector in price_selectors:
                        try:
                            price_element = driver.find_element(By.CSS_SELECTOR, price_selector)
                            product_price = price_element.text or price_element.get_attribute("innerHTML")
                            if product_price:
                                print(f"Product Price: {product_price}")
                                break
                        except NoSuchElementException:
                            continue
                except Exception as e:
                    print(f"Error finding price: {str(e)}")
                    product_price = "Unknown"
                
                # 5. Add the product to the cart
                print("Attempting to add product to cart...")
                try:
                    add_button = driver.find_element(By.ID, "add-to-cart-button")
                    driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
                    time.sleep(2)
                    driver.execute_script("arguments[0].click();", add_button)
                    print("Clicked Add to Cart button using JavaScript")
                    time.sleep(3)  # Wait for add-to-cart action to complete
                except (NoSuchElementException, StaleElementReferenceException):
                    print("Could not find Add to Cart button")
                
                print("Product added to cart successfully.")
                success = True
                break  # Exit the retry loop
            
            except Exception as e:
                print(f"Error with product #{attempt_count}: {str(e)}")
                driver.get(search_url)
                time.sleep(3)
                attempt_count += 1
        
        if not success:
            print(f"\nFailed to add any product to cart after trying {products_tried} products")
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    amazon_product_search_and_cart()

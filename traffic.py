from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

BASE_URL = 'http://127.0.0.1:5000'

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1920, 1080)
    return driver

def signup(driver, username, email, password, plan='Free'):
    try:
        driver.get(f'{BASE_URL}/signup')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
        logging.debug(f'Filling signup form for {username}')
        
        # Fill the form
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'email').send_keys(email)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.NAME, 'password2').send_keys(password)
        
        # Select plan
        plan_button = driver.find_element(By.CSS_SELECTOR, f"div#card_{plan.lower()} button")
        driver.execute_script("arguments[0].click();", plan_button)
        
        # Submit the form
        submit_button = driver.find_element(By.CSS_SELECTOR, "form button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Check if user is redirected to a success page or profile page
        WebDriverWait(driver, 20).until(EC.url_contains('/profile'))
        logging.info(f'Successfully signed up {username}')
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        logging.error(f'Error during signup for {username}: {e}')
        driver.save_screenshot(f'signup_error_{username}.png')
        with open(f'signup_page_source_{username}.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        raise


def login(driver, username, password):
    try:
        driver.get(f'{BASE_URL}/login')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
        logging.debug(f'Logging in {username}')
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password)
        submit_button = driver.find_element(By.CSS_SELECTOR, "form button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 20).until(EC.url_to_be(f'{BASE_URL}/'))
        logging.info(f'Logged in {username}')
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        logging.error(f'Login failed for {username}: {e}')
        driver.save_screenshot(f'login_error_{username}.png')

def search(driver, query):
    try:
        driver.get(BASE_URL)  # Ensure we are on the homepage
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'query')))
        logging.debug(f'Searching for {query}')
        search_box = driver.find_element(By.NAME, 'query')
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for the search results to load
        logging.debug('Waiting for search results to load')
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card')))
            logging.info(f'Search results loaded for {query}')
        except Exception as e:
            logging.error(f'Error: Search results did not load for {query}: {e}')
            driver.save_screenshot(f'search_results_error_{query}.png')
            with open(f'page_source_{query}.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            raise

        time.sleep(random.uniform(1, 3))
    except Exception as e:
        logging.error(f'Error during search for {query}: {e}')
        driver.save_screenshot(f'search_error_{query}.png')


def change_plan(driver, plan):
    try:
        driver.get(f'{BASE_URL}/profile')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"div#card_{plan.lower()} button")))
        logging.debug(f'Changing plan to {plan}')
        plan_button = driver.find_element(By.CSS_SELECTOR, f"div#card_{plan.lower()} button")
        driver.execute_script("arguments[0].click();", plan_button)
        submit_button = driver.find_element(By.CSS_SELECTOR, "form button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        logging.info(f'Changed plan to {plan}')
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        logging.error(f'Error during plan change to {plan}: {e}')
        driver.save_screenshot(f'change_plan_error.png')

def main():
    driver = setup_driver()
    try:
        for i in range(1, 11):
            username = f'user{i}'
            email = f'user{i}@example.com'
            password = 'password123'
            signup(driver, username, email, password)
            # Comment out the login and search steps for now
            # login(driver, username, password)
            # search(driver, 'Inception')
            # change_plan(driver, 'Premium' if i % 2 == 0 else 'Free')
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

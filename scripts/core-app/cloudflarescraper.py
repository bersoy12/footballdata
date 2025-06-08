import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import json
import numpy as np
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

class CloudflareScraper:
    def __init__(self):
        self.driver = None
        self.env = load_dotenv()
        
    def start_browser(self):
        """Tarayıcıyı başlatır ve Cloudflare korumasını atlatır"""
        if self.driver is not None:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
            
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-setuid-sandbox')
        
        if os.environ.get('DOCKER_ENV'):
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-accelerated-2d-canvas')
            options.add_argument('--no-first-run')
            options.add_argument('--no-zygote')
            options.add_argument('--single-process')
            options.add_argument('--disable-features=site-per-process')

        service = Service(log_path='chrome_driver.log')
        service.service_args = ['--log-level=0'] 
        
        self.driver = uc.Chrome(options=options, service=service)
        self.driver.set_page_load_timeout(30)
        
    def scrape_website(self, url):
        """Belirtilen URL'den veri çeker"""
        try:
            
            self.start_browser()
            logger.info(f"GET request to URL: {url}")
            self.driver.get(url)
            time.sleep(5)
            
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            content = self.driver.page_source
            logger.info("The page content has been retrieved successfully.")
            if '<pre>' in content:
                soup = BeautifulSoup(content, "html.parser")
                pre_text = soup.find('pre').text
                content = json.loads(pre_text)
            
            return content
            
        except Exception as e:
            logger.error(f"Error during request to {url}: {str(e)}")
            return None
            
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
    
    def __del__(self):
        """Destructor - tarayıcıyı temiz bir şekilde kapatır"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None



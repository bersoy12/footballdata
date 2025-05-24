import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import numpy as np
from bs4 import BeautifulSoup
from dotenv import load_dotenv


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
        
        self.driver = uc.Chrome(options=options)
        self.driver.set_page_load_timeout(30)
        
    def scrape_website(self, url):
        """Belirtilen URL'den veri çeker"""
        try:
            self.start_browser()
            print("Sayfa yükleniyor...")
            
            self.driver.get(url)
            time.sleep(5)
            
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            content = self.driver.page_source
            print("Sayfa içeriği başarıyla alındı")
            if '<pre>' in content:
                soup = BeautifulSoup(content, "html.parser")
                pre_text = soup.find('pre').text
                content = json.loads(pre_text)
            
            return content
            
        except Exception as e:
            print(f"Hata oluştu: {str(e)}")
            return None
            
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
                print("Tarayıcı kapatıldı")
    
    def __del__(self):
        """Destructor - tarayıcıyı temiz bir şekilde kapatır"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None



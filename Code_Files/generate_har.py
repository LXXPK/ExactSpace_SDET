from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
import time
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  

bmp_path = r"C:\Users\reddy\Desktop\SDET_assignment\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat"
server = Server(bmp_path, options={'port': 9090}) 
server.start()
proxy = server.create_proxy()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--proxy-server={proxy.proxy}")
chrome_options.add_argument("--ignore-certificate-errors")  
chrome_options.add_argument("--allow-insecure-localhost")   
chrome_options.add_argument("--disable-web-security")      
chrome_options.add_argument("--no-sandbox")               
chrome_options.add_argument("--disable-gpu")               
chrome_options.add_argument("--log-level=3")               
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--v=0")  
chrome_options.add_argument("--headless=new")  

service = Service(r"C:\Users\reddy\Desktop\SDET_assignment\chromedriver-win64\chromedriver.exe")  
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    proxy.new_har("exactspace")
    
    url = "https://exactspace.co/ "
    driver.get(url)
    time.sleep(10)  

    har_data = proxy.har
    with open("output.har", "w") as har_file:
        json.dump(har_data, har_file)
finally:
    driver.quit()
    server.stop()
    print("Har file generated successfully")

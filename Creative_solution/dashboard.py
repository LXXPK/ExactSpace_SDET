import streamlit as st
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
import time
import os
import matplotlib.pyplot as plt
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  
os.environ['CUDA_VISIBLE_DEVICES'] = '-1' 


bmp_path = r"C:\Users\reddy\Desktop\SDET_assignment\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat"  
chromedriver_path = r"C:\Users\reddy\Desktop\SDET_assignment\chromedriver-win64\chromedriver.exe"  


def generate_har(url, output_file="output.har"):
    """Generates a HAR file for the given URL."""
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

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        proxy.new_har("site")
        driver.get(url)
        time.sleep(10)  

        har_data = proxy.har
        with open(output_file, "w") as har_file:
            json.dump(har_data, har_file)
    finally:
        driver.quit()
        server.stop()

    return output_file


def parse_har(file_content):
    """Parses HAR file for key metrics."""
    har_data = json.loads(file_content)

    status_2xx, status_4xx, status_5xx = 0, 0, 0
    total_response_size = 0
    response_times = []
    failed_requests = []
    largest_payload = {"url": None, "size": 0}

    for entry in har_data["log"]["entries"]:
        status_code = entry["response"]["status"]
        if 200 <= status_code < 300:
            status_2xx += 1
        elif 400 <= status_code < 500:
            status_4xx += 1
            failed_requests.append(entry["request"]["url"])
        elif 500 <= status_code < 600:
            status_5xx += 1
            failed_requests.append(entry["request"]["url"])

        response_times.append(entry["time"])
        response_size = entry["response"]["bodySize"]
        total_response_size += response_size
        if response_size > largest_payload["size"]:
            largest_payload = {"url": entry["request"]["url"], "size": response_size}

    avg_response_time = sum(response_times) / len(response_times) if response_times else 0

    return {
        "status_2xx": status_2xx,
        "status_4xx": status_4xx,
        "status_5xx": status_5xx,
        "average_response_time": avg_response_time,
        "total_response_size": total_response_size,
        "failed_requests": failed_requests,
        "largest_payload": largest_payload,
    }

#Generates Matplotlib visualizations from metrics.------------------------------------------------------------------
def visualize_data(metrics):
    statuses = ["2XX", "4XX", "5XX"]
    counts = [metrics["status_2xx"], metrics["status_4xx"], metrics["status_5xx"]]
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    ax[0].pie(counts, labels=statuses, autopct='%1.1f%%', startangle=140)
    ax[0].set_title("Response Status Distribution")

    ax[1].bar(statuses, counts, color=["green", "orange", "red"])
    ax[1].set_title("Response Status Count")
    ax[1].set_ylabel("Count")
    ax[1].set_xlabel("Status Code")

    return fig

st.image(r"C:\Users\reddy\Desktop\SDET_assignment\logo.png",width=150, use_container_width=True)
st.title("Interactive HAR Analysis Dashboard")


st.header("1. Generate HAR File")
url = st.text_input("Enter URL:")
if st.button("Generate HAR"):
    try:
        har_file_path = generate_har(url)
        st.success(f"HAR file generated successfully: {har_file_path}")
        with open(har_file_path, "rb") as file:
            st.download_button("Download HAR File", file, "output.har", "application/octet-stream")
    except Exception as e:
        st.error(f"Error generating HAR file: {e}")


st.header("2. Analyze HAR File")
uploaded_file = st.file_uploader("Upload HAR File", type=["har"])
if uploaded_file:
    try:
        file_content = uploaded_file.read()
        metrics = parse_har(file_content)

       
        st.subheader("Key Metrics")
        st.json(metrics)

        
        st.subheader("Visualizations")
        chart = visualize_data(metrics)
        st.pyplot(chart)
    except Exception as e:
        st.error(f"Error parsing HAR file: {e}")

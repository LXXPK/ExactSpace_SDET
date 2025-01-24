# Kiran BodiReddy - SDET Assessment

This repository contains the complete implementation for an SDET internship assessment. The project includes the following main functionalities:

1. Generating a `.har` file using `generate_har.py`.
2. Parsing the generated `.har` file to count status codes (2XX, 4XX, 5XX) using `parse_har.py`.
3. An interactive dashboard (`dashboard.py`) built with Streamlit for a user-friendly interface that combines all functionalities in one place.



## Features

1. **Standalone Scripts**:
    - Use `generate_har.py` to generate a HAR file by visiting a specified URL.
    - Use `parse_har.py` to analyze the HAR file and output the count of status codes (2XX, 4XX, 5XX).

2. **Interactive Dashboard**:
    - Run `dashboard.py` to access a web-based interface for all functionalities.
    - Easily upload and analyze HAR files or generate them directly without running standalone scripts.

## Installation and Requirements

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-repository/Kiran_BodiReddy_SDET.git
    cd Kiran_BodiReddy_SDET
    ```

2. **Install Python dependencies**:
    Install the required libraries from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

3. **Additional Requirements**:
    - Install `Google Chrome` and the `ChromeDriver` binary. Ensure the `chromedriver` version matches your installed Chrome version.
    - [Download ChromeDriver here](https://chromedriver.chromium.org/downloads).
    - Download and set up browsermob-proxy 
    - [Download browsermob-proxy here](https://github.com/lightbody/browsermob-proxy/releases)

## Usage

### Option 1: Standalone Scripts

1. **Generate a HAR File**:
    ```bash
    python generate_har.py
    ```
    Follow the on-screen instructions to specify a URL and save the `.har` file.

2. **Parse the HAR File**:
    ```bash
    python parse_har.py
    ```
    Follow the on-screen instructions to specify the path to the `.har` file and view the output.

### Option 2: Streamlit Dashboard

1. Run the dashboard:
    ```bash
    streamlit run dashboard.py
    ```
    This will launch an interactive web application in your default web browser.

2. Features available via the dashboard:
    - Generate a new `.har` file by specifying the target URL.
    - Upload an existing `.har` file and analyze its status codes.
    - Download the generated `.har` file and view the parsed results directly.

## Example Outputs

- **Generated HAR File**: See `Generated_har.har` for a sample HAR file generated using the project.
- **Parsed Output**: See `Output.txt` for a sample of the parsed results, showing counts of HTTP status codes.



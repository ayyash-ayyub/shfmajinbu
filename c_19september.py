from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import csv

# Function to scrape a news website
def scrape_news(url, title_selector, content_selector, date_selector):
    # Chrome Driver setup
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless browser
    service = Service("path_to_chromedriver")  # Replace with your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Access the URL
    driver.get(url)
    time.sleep(3)  # Allow page to load
    
    # Scraping title, content, and date based on the provided selectors
    try:
        title = driver.find_element(By.CSS_SELECTOR, title_selector).text
    except:
        title = "Title not found"

    try:
        content = driver.find_element(By.CSS_SELECTOR, content_selector).text
    except:
        content = "Content not found"

    try:
        date = driver.find_element(By.CSS_SELECTOR, date_selector).text
    except:
        date = "Date not found"
    
    # Close the driver
    driver.quit()

    # Return the results as a dictionary
    return {
        'Title': title,
        'Content': content,
        'Date': date
    }

# Function to write the data to a CSV file
def save_to_csv(data, filename='scraped_news.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Content', 'Date'])
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")

# Main function to configure the scraping
def main():
    url = input("Enter the news URL: ")
    title_selector = input("Enter CSS selector for the title: ")
    content_selector = input("Enter CSS selector for the content: ")
    date_selector = input("Enter CSS selector for the date: ")

    news_data = scrape_news(url, title_selector, content_selector, date_selector)
    
    # Save to CSV
    save_to_csv([news_data])

if __name__ == "__main__":
    main()

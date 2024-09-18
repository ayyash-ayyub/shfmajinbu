import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import pandas as pd

# Function to scrape full article content from detail page
def scrape_full_article(url, content_tag_selector):
    #response = requests.get(url)
    try:
        # Configure WebDriver to use headless Firefox
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)


        # Get the URL given
        driver.get(url)
 
        # Selenium will wait for a maximum of 5 seconds for an element matching the given criteria to be found. 
        # If no element is found in that time, Selenium will raise an error.
        try:
            wait = WebDriverWait(driver, timeout=5)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, content_tag_selector)))
        except:
            raise LookupError("There is no element specified")
        

        # BeautifulSoup will parse the URL
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        #soup = BeautifulSoup(response.text, 'html.parser')

        # Find the full content within the specified content tag (e.g., 'div.entry-content')
        content_tag = soup.select_one(content_tag_selector)
        if content_tag:
            paragraphs = content_tag.find_all('p')
            full_content = ' '.join([para.get_text(separator=' ').strip() for para in paragraphs])
        else:
            full_content = 'No content'

        # Close the WebDriver
        driver.quit()
        return full_content
    
    except Exception as e:
        # Print the error message
        print('An error occurred: ', e)
        # Close the WebDriver
        driver.quit()

# Function to dynamically detect title and link from a page
def scrape_page(url, site_config):
    try:
        # Configure WebDriver to use headless Firefox
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
        #print(url)
        #print(site_config['indicator'])


        # Get the URL given
        driver.get(url)
 
        # Selenium will wait for a maximum of 5 seconds for an element matching the given criteria to be found. 
        # If no element is found in that time, Selenium will raise an error.
        try:
            wait = WebDriverWait(driver, timeout=10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, site_config['indicator'])))
        except:
            raise LookupError("There is no element specified")
        

        # BeautifulSoup will parse the URL
        content = driver.page_source
        #print(content)
        #print("-----------------")
        soup = BeautifulSoup(content, 'html.parser')
        articles = []
        #print(soup.select(site_config['article_selector']))

        #print("-------articles----------")
        # Dynamically detect articles based on the site's configuration
        #for article in soup.select(site_config['article_selector']):
            # Scrape title
        title_tag = soup.select_one(site_config['title_selector'])
        title = title_tag.text.strip() if title_tag else 'No title'

        # Scrape article detail page link
        detail_link_tag = title_tag.find('a') if title_tag else None
        detail_link = detail_link_tag['href'] if detail_link_tag else None

        # Scrape date if date_selector is provided
        date_tag = soup.select_one(site_config.get('date_selector', ''))
        date = date_tag.text.strip() if date_tag else 'No date'
        
        content_tag = soup.select_one(site_config.get('content_selector', ''))
        if content_tag:
            paragraphs = content_tag.find_all('p')
            full_content = ' '.join([para.get_text(separator=' ').strip() for para in paragraphs])
        else:
            full_content = 'No content'

        # If detail link exists, scrape full content from the detail page
        # if detail_link:
        #     full_content = scrape_full_article(detail_link, site_config['content_selector'])
        # else:
        #     full_content = 'No content'
        
        #print(full_content)

        # Add article data to list
        articles.append({
            'title': title,
            'content': full_content,
            'date': date
        })

        # Close the WebDriver
        driver.quit()
        
        return articles
    
    except Exception as e:
        # Print the error message
        print('An error occurred: ', e)
        # Close the WebDriver
        driver.quit()

    #response = requests.get(url)
    #soup = BeautifulSoup(response.text, 'html.parser')

# Function to handle pagination and scrape all pages
def scrape_website(base_url, site_config, max_articles=100):
    page = 1
    all_articles = []
    
    while len(all_articles) < max_articles:
        url = f"{base_url}/page/{page}/"
        print(f"Scraping page {page}: {url}")
        
        articles = scrape_page(url, site_config)
        
        # Stop if no articles found (end of pagination)
        if not articles:
            break
        
        all_articles.extend(articles)
        
        # If more than max_articles, trim the list
        if len(all_articles) > max_articles:
            all_articles = all_articles[:max_articles]
            break
        
        page += 1

    return all_articles

# Define configurations for different websites
site_configs = {
    # 'krebsonsecurity': {
    #     'base_url': 'https://krebsonsecurity.com',
    #     'article_selector': 'article', 
    #     'indicator': 'entry-title', 
    #     'title_selector': 'h2.entry-title', 
    #     'date_selector': 'div.adt', 
    #     'content_selector': 'div.entry-content' 
    # },

    'kompas': {
        'base_url': 'https://nasional.kompas.com/read/2024/09/17/05531201/bubarkan-diri-jamaah-islamiyah-minta-maaf-ke-negara-dan-publik',
        'article_selector': 'article', 
        'indicator': 'read__title', 
        'title_selector': 'h1.read__title', 
        'date_selector': 'div.read__time', 
        'content_selector': 'div.read__content' 
    },
 
}

# Choose which site to scrape
selected_site = 'kompas'  # Change this to 'thehackernews' to scrape that site

# Scrape a maximum of 100 articles
site_config = site_configs[selected_site]
articles = scrape_page(site_config['base_url'], site_config)
#articles = scrape_website(site_config['base_url'], site_config, max_articles=50)
print(articles)
# Create DataFrame and export to Excel
df = pd.DataFrame(articles)
df.to_excel(f'{selected_site}_scraped_data_full_content.xlsx', index=False)

print(f"Data successfully scraped and exported to {selected_site}_scraped_data_full_content.xlsx")



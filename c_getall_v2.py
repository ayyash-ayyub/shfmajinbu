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
    try:
        # Configure WebDriver to use headless Firefox
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)

        driver.get(url)

        # Wait for the article content to load
        try:
            wait = WebDriverWait(driver, timeout=10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, content_tag_selector)))
        except Exception:
            raise LookupError("Content not found in the article page.")

        # BeautifulSoup parses the page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content_tag = soup.select_one(content_tag_selector)
        
        # Extract the full article content
        if content_tag:
            paragraphs = content_tag.find_all('p')
            full_content = ' '.join([para.get_text(separator=' ').strip() for para in paragraphs])
        else:
            full_content = 'No content'

        driver.quit()
        return full_content
    
    except Exception as e:
        print(f'Error scraping full article: {e}')
        driver.quit()
        return 'No content'

# Function to scrape article list and content from a page
def scrape_page(url, site_config):
    try:
        # Configure WebDriver to use headless Firefox
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)

        driver.get(url)

        # Wait for the article list to load
        try:
            wait = WebDriverWait(driver, timeout=10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, site_config['indicator'])))
        except Exception:
            raise LookupError("No articles found on this page.")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = []

        # Loop through the articles
        for article in soup.select(site_config['article_selector']):
            # Scrape title
            title_tag = article.select_one(site_config['title_selector'])
            title = title_tag.get_text(strip=True) if title_tag else 'No title'

            # Scrape detail link
            detail_link_tag = title_tag.find('a') if title_tag else None
            detail_link = detail_link_tag['href'] if detail_link_tag else None
            if detail_link and not detail_link.startswith('http'):
                detail_link = site_config['base_url'] + detail_link

            # Scrape date
            date_tag = article.select_one(site_config.get('date_selector', ''))
            if date_tag:
                date = date_tag.get_text(strip=True)
            else:
                # Check if the date is available in another tag
                date = 'No date'
                print(f"Date not found for article: {title}")

            # Scrape content or full article from the detail link
            if detail_link:
                full_content = scrape_full_article(detail_link, site_config['content_selector'])
            else:
                full_content = 'No content'

            articles.append({
                'title': title,
                'content': full_content,
                'date': date
            })

        driver.quit()
        return articles
    
    except Exception as e:
        print(f'Error scraping page: {e}')
        driver.quit()
        return []

# Function to handle pagination and scrape all pages
def scrape_website(base_url, site_config, max_articles=100):
    page = 1
    all_articles = []
    
    while len(all_articles) < max_articles:
        url = f"{base_url}/page/{page}/"
        print(f"Scraping page {page}: {url}")
        
        articles = scrape_page(url, site_config)
        
        if not articles:
            break
        
        all_articles.extend(articles)
        
        if len(all_articles) >= max_articles:
            break
        
        page += 1

    return all_articles[:max_articles]

# Define configurations for different websites
site_configs = {
    'kompas': {
        'base_url': 'https://nasional.kompas.com',
        'article_selector': 'div.article__list',
        'indicator': 'article__title',
        'title_selector': 'h3.article__title',
        'date_selector': 'div.article__date',  # Ensure this is correct by inspecting HTML
        'content_selector': 'div.read__content'
    },
}

# Choose which site to scrape
selected_site = 'kompas'

# Scrape articles
site_config = site_configs[selected_site]
articles = scrape_website(site_config['base_url'], site_config, max_articles=10)

# Create DataFrame and export to Excel
df = pd.DataFrame(articles)
df.to_excel(f'{selected_site}_scraped_data_full_content.xlsx', index=False)

print(f"Data successfully scraped and exported to {selected_site}_scraped_data_full_content.xlsx")

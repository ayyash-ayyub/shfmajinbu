import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape full article content from detail page
def scrape_full_article(url, content_tag_selector):
    print(f"Scraping full article from: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the full content within the specified content tag (e.g., 'div.ContentModule-Wrapper')
    content_tag = soup.select_one(content_tag_selector)
    if content_tag:
        # Collect all paragraphs inside the content tag
        paragraphs = content_tag.find_all('p')
        # Join all paragraphs into one string
        full_content = ' '.join([para.get_text(separator=' ').strip() for para in paragraphs])
        if not full_content.strip():
            full_content = 'No content'  # In case the content is empty
    else:
        full_content = 'No content found'

    return full_content

# Function to scrape a single page
def scrape_page(url, site_config):
    print(f"Scraping page: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []

    # Find all article blocks
    for article in soup.select(site_config['article_selector']):
        # Scrape title
        title_tag = article.select_one(site_config['title_selector'])
        if title_tag:
            title = title_tag.text.strip()
            print(f"Title found: {title}")
        else:
            title = 'No title'
            print("No title found")
        
        # Scrape article detail page link
        detail_link_tag = article.select_one('a')  # We look for <a> directly inside the article
        if detail_link_tag and 'href' in detail_link_tag.attrs:
            detail_link = detail_link_tag['href']
            if not detail_link.startswith('http'):
                detail_link = f"{site_config['base_url']}{detail_link}"
            print(f"Detail link found: {detail_link}")
        else:
            detail_link = None
            print("No detail link found")

        # If detail link exists, scrape full content from the detail page
        if detail_link:
            full_content = scrape_full_article(detail_link, site_config['content_selector'])
        else:
            full_content = 'No content'

        # Add article data to list
        articles.append({
            'title': title,
            'content': full_content
        })

    return articles

# Function to handle pagination and scrape all pages
def scrape_website(site_config, max_articles=100):
    page = 1
    all_articles = []

    while len(all_articles) < max_articles:
        # Using dynamic pagination URL from site_config
        url = site_config['base_url'].format(page=page)
        print(f"Scraping page {page}: {url}")
        
        articles = scrape_page(url, site_config)
        
        if not articles:
            break
        
        all_articles.extend(articles)
        
        if len(all_articles) > max_articles:
            all_articles = all_articles[:max_articles]
            break
        
        page += 1

    return all_articles

# Define configurations with pagination URL pattern
site_config = {
        'base_url': 'https://krebsonsecurity.com/page/{page}/?s=security',
        'article_selector': 'article', 
        'title_selector': 'h2.entry-title', 
        'content_selector': 'div.entry-content' 
    }

# Scrape a maximum of 100 articles
articles = scrape_website(site_config, max_articles=100)

# Create DataFrame and export to Excel
df = pd.DataFrame(articles)
df.to_excel('darkreading_scraped_data_full_content.xlsx', index=False)

print(f"Data successfully scraped and exported to darkreading_scraped_data_full_content.xlsx")

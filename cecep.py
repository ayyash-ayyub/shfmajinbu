import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib.parse

def get_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve {url}: Status code {response.status_code}")
    except Exception as e:
        print(f"Error retrieving {url}: {str(e)}")
    return None

def parse_content(html_content, url):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Ambil judul halaman
    if soup.title:
        title = soup.title.string
    else:
        title = 'No Title'

    # Ambil konten teks halaman
    content = soup.get_text(separator=' ', strip=True)

    # Ambil tahun dari URL atau konten
    year_match = re.search(r'(20\d{2})', url + content)
    year = year_match.group(0) if year_match else 'Unknown'

    return title, content[:500], year

def find_internal_links(soup, base_url):
    """
    Mencari semua tautan internal di halaman.
    """
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/'):
            href = urllib.parse.urljoin(base_url, href)
        elif urllib.parse.urlparse(href).netloc == '':
            href = urllib.parse.urljoin(base_url, href)
        if base_url in href:
            links.append(href)
    return set(links)  # Menggunakan set untuk menghindari duplikasi

def scrape_all_pages(base_url):
    """
    Scraping semua halaman dari website.
    """
    visited_urls = set()
    all_data = []
    urls_to_scrape = [base_url]

    while urls_to_scrape:
        current_url = urls_to_scrape.pop(0)
        if current_url in visited_urls:
            continue

        print(f"Scraping {current_url}")
        html_content = get_page_content(current_url)
        if html_content:
            visited_urls.add(current_url)
            title, content, year = parse_content(html_content, current_url)

            # Simpan data jika ada
            if title and content:
                all_data.append({'Title': title, 'Content': content, 'Year': year})

            # Temukan tautan internal dan tambahkan ke antrian
            soup = BeautifulSoup(html_content, 'html.parser')
            internal_links = find_internal_links(soup, base_url)
            for link in internal_links:
                if link not in visited_urls and link not in urls_to_scrape:
                    urls_to_scrape.append(link)

    return all_data

# URL dasar untuk website yang akan di-scrape
base_url = 'https://ut.ac.id/'

# Menampung hasil scraping dari semua halaman
all_data = scrape_all_pages(base_url)

# Simpan hasil ke file CSV
df = pd.DataFrame(all_data)
df.to_csv('seamolec.csv', index=False)

print("done.csv")

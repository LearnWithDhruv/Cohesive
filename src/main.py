from bs4 import BeautifulSoup
import requests
import re

def scrape_website(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        contact_selectors = [
            'footer', '.contact', '#contact', '.footer',
            '.email', '#email', 'address', '.address'
        ]
        
        contact_content = []
        for selector in contact_selectors:
            contact_content.extend([el.get_text() for el in soup.select(selector)])
        
        main_content = " ".join([t for t in soup.stripped_strings])
        prioritized_content = " ".join(contact_content) + " " + main_content
        
        return prioritized_content
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

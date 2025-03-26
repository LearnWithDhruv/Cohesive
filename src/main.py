from scraper import scrape_website
from ai_enrichment import enrich_data
from contact_validator import extract_and_validate_contacts
from sheets_integration import read_sheet, write_sheet
import time

def process_row(url, query):
    print(f"\nProcessing: {url}")
    print(f"Query: {query}")
    
    content = None
    for _ in range(2):  
        content = scrape_website(url)
        if content:
            break
        time.sleep(1)
    
    if not content:
        print("! Failed to scrape content")
        return [url, query, "NO", "N/A", "N/A"]
    
    print(f"Scraped content length: {len(content)} chars")
    
    answer = enrich_data(content, query)
    
    emails, phones = [], []
    try:
        emails, phones = extract_and_validate_contacts(content)
        print(f"Found {len(emails)} email(s) and {len(phones)} phone(s)")
    except Exception as e:
        print(f"Contact extraction error: {e}")
    
    return [
        url,
        query,
        answer,
        ", ".join(emails) if emails else "N/A",
        ", ".join(phones) if phones else "N/A"
    ]

def main():
    sheet_data = read_sheet()
    results = []
    
    for row in sheet_data:
        if len(row) >= 2:
            result = process_row(row[0], row[1])
            results.append(result)
            time.sleep(1)  
    
    write_sheet(results)

if __name__ == "__main__":
    main()

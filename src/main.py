# src/main.py
from sheets_integration import read_sheet, write_sheet
from scraper import scrape_website
from ai_enrichment import enrich_data
from contact_validator import extract_and_validate_contacts
CONFIDENCE_THRESHOLD = 0.7 
def main():
    sheet_data = read_sheet()
    
    results = []
    for row in sheet_data:
        url = row[0]  
        query = row[1]  

        content = scrape_website(url)
        if not content:
            results.append([url, query, "Website not accessible", "", ""])
            continue
        
        answer = enrich_data(content, query)
        
        emails, phones = extract_and_validate_contacts(content)
        print(f"Final extracted for {url}: Answer: {answer}, Emails: {emails}, Phones: {phones}")
        
        emails_str = ", ".join(emails) if emails else ""
        phones_str = ", ".join(phones) if phones else ""
        result_row = [url, query, answer, emails_str, phones_str]
        print(f"Result row to write: {result_row}")
        results.append(result_row)
    
    print(f"Writing results to Google Sheet: {results}")
    write_sheet(results)

if __name__ == "__main__":
    main()
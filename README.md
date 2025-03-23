# README

## Project Overview
This project automates the process of extracting, validating, and enriching data from websites based on user queries. It integrates multiple components, including web scraping, AI-driven question answering, contact validation, and Google Sheets integration for data storage and retrieval.

## Project Structure
The project consists of multiple Python modules:

- `ai_enrichment.py` - Uses an AI model to determine relevant information from extracted text.
- `contact_validator.py` - Extracts and validates email addresses and phone numbers from web content.
- `main.py` - Main script orchestrating the workflow.
- `scraper.py` - Web scraping utility to fetch textual content from websites.
- `sheets_integration.py` - Handles reading and writing data to Google Sheets.

---

## Installation and Setup
### Prerequisites
Ensure you have Python 3.8+ installed and set up a virtual environment if needed.

### Required Dependencies
Install the necessary dependencies using:
```sh
pip install -r requirements.txt
```

Dependencies include:
- `transformers` (for AI-based enrichment)
- `beautifulsoup4` (for web scraping)
- `requests` (for making HTTP requests)
- `email-validator` (for validating emails)
- `phonenumbers` (for validating phone numbers)
- `gspread` (for Google Sheets integration)
- `google-auth` (for authentication with Google services)

---

## Module Details
### `ai_enrichment.py`
This module enriches extracted web content by answering a user-provided query using an AI model (`distilbert-base-uncased-distilled-squad`). If the AI confidence score is above `0.3` and relevant keywords exist in the content, it returns `Yes`; otherwise, it returns `No`.

#### Function: `enrich_data(content, query)`
- **Parameters:**
  - `content` (str): Extracted website text.
  - `query` (str): User query.
- **Returns:** `'Yes'` if relevant information is found; otherwise, `'No'`.

### `contact_validator.py`
Extracts and validates email addresses and phone numbers from text content.

#### Function: `extract_and_validate_contacts(content)`
- **Parameters:**
  - `content` (str): Extracted website text.
- **Returns:**
  - `valid_emails` (list): Valid email addresses.
  - `valid_phones` (list): Valid phone numbers.

### `scraper.py`
Fetches website content and removes non-text elements.

#### Function: `scrape_website(url)`
- **Parameters:**
  - `url` (str): Website URL.
- **Returns:** Extracted clean text or `None` if an error occurs.

### `sheets_integration.py`
Handles interaction with Google Sheets.

#### Function: `read_sheet()`
- Reads data from a Google Sheet (`CohesivePrototype`).
- Returns a list of rows containing URLs and queries.

#### Function: `write_sheet(results)`
- Writes results to the Google Sheet.

### `main.py`
The main orchestrator that:
1. Reads data from Google Sheets.
2. Scrapes website content.
3. Enriches the data using AI.
4. Extracts and validates contact information.
5. Writes the results back to Google Sheets.

#### Constants:
- `CONFIDENCE_THRESHOLD = 0.7` (Determines when an answer is considered relevant)

#### Execution:
Run the script using:
```sh
python src/main.py
```

---

## Google Sheets Integration
1. **Create Google Service Account Credentials:**
   - Generate a service account key from Google Cloud Console.
   - Save the `credentials.json` file in `config/credentials.json`.
   - Share the Google Sheet with the service account email.

2. **Google Sheets Permissions:**
   - Ensure the service account has "Editor" access to the sheet.

---

## Error Handling
- **Scraper Errors:** Logs failed requests and returns `None`.
- **AI Model Errors:** Ensures the response is always handled safely.
- **Google Sheets Errors:** Captures exceptions when reading/writing data.

---

## Future Enhancements
- Implement caching to reduce repeated scraping.
- Enhance AI model customization.
- Improve phone number formatting for different countries.

---

## Author
Developed by [Your Name].

For questions, contact [your.email@example.com].

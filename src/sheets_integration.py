import gspread
from google.oauth2.service_account import Credentials
import os
from google.auth.exceptions import RefreshError

def authenticate():
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        credentials_path = "config/credentials.json"
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Credentials file not found at {credentials_path}")
            
        creds = Credentials.from_service_account_file(
            credentials_path,
            scopes=scopes
        )
        
        if creds.expired:
            creds.refresh()
            
        return gspread.Client(auth=creds)
    except Exception as e:
        print(f"Authentication failed: {e}")
        raise

def read_sheet():
    try:
        client = authenticate()
        sheet = client.open("CohesivePrototype").sheet1
        data = sheet.get("A2:B")
        return data if data else []
    except gspread.exceptions.SpreadsheetNotFound:
        print("Error: Google Sheet 'CohesivePrototype' not found")
        return []
    except Exception as e:
        print(f"Error reading from Google Sheets: {e}")
        return []

def write_sheet(results):
    try:
        client = authenticate()
        sheet = client.open("CohesivePrototype").sheet1
        
        headers = ["URL", "Query", "Answer", "Emails", "Phones"]
        sheet.update("A1:E1", [headers])
        
        if results:
            sheet.update(f"A2:E{len(results) + 1}", results)
        else:
            print("No results to write")
            
    except gspread.exceptions.SpreadsheetNotFound:
        print("Error: Google Sheet 'CohesivePrototype' not found")
    except Exception as e:
        print(f"Error writing to Google Sheets: {e}")

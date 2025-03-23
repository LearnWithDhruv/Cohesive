# src/sheets_integration.py
import gspread
from google.oauth2.service_account import Credentials

def read_sheet():
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",  
            "https://www.googleapis.com/auth/drive"         
        ]
        
        creds = Credentials.from_service_account_file("config/credentials.json", scopes=scopes)
        
        client = gspread.Client(auth=creds)
        
    
        sheet = client.open("CohesivePrototype").sheet1
        
        data = sheet.get("A2:B")
        return data
    except Exception as e:
        print(f"Error reading from Google Sheets: {e}")
        return []

def write_sheet(results):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets", 
            "https://www.googleapis.com/auth/drive"         
        ]
        
        creds = Credentials.from_service_account_file("config/credentials.json", scopes=scopes)
        
        client = gspread.Client(auth=creds)
        
        sheet = client.open("CohesivePrototype").sheet1
        
        headers = ["URL", "Query", "Answer", "Emails", "Phones"]
        sheet.update("A1:E1", [headers])
        
        sheet.update("A2:E", results)
    except Exception as e:
        print(f"Error writing to Google Sheets: {e}")
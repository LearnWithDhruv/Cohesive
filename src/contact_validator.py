# src/contact_validator.py
import re
from email_validator import validate_email, EmailNotValidError
import phonenumbers

def extract_and_validate_contacts(content):
    if not content or not isinstance(content, str):
        return [], []
    
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    extracted_emails = re.findall(email_pattern, content)
    valid_emails = []
    
    for email in extracted_emails:
        try:
            validate_email(email, check_deliverability=False) 
            valid_emails.append(email)
        except EmailNotValidError:
            continue  

    phone_pattern = r"\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    extracted_phones = re.findall(phone_pattern, content)
    valid_phones = []
    
    for phone in extracted_phones:
        try:
            parsed_phone = phonenumbers.parse(phone, None)
            if phonenumbers.is_valid_number(parsed_phone):
                valid_phones.append(phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
        except phonenumbers.NumberParseException:
            continue  
    
    return valid_emails, valid_phones

import re
from email_validator import validate_email, EmailNotValidError
import phonenumbers

def extract_emails_with_fallbacks(content):
    email_patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        r'\b[A-Za-z0-9._%+-]+\[at\][A-Za-z0-9.-]+\[dot\][A-Za-z]{2,}\b',
        r'\b[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\s*\.\s*[A-Za-z]{2,}\b',
        r'\b[A-Za-z0-9._%+-]+\s*\(\s*at\s*\)\s*[A-Za-z0-9.-]+\s*\(\s*dot\s*\)\s*[A-Za-z]{2,}\b'
    ]
    
    emails = set()
    for pattern in email_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            clean_email = (match.replace('[at]', '@')
                          .replace('[dot]', '.')
                          .replace('(at)', '@')
                          .replace('(dot)', '.')
                          .replace(' ', ''))
            try:
                valid = validate_email(clean_email, check_deliverability=False)
                emails.add(valid.normalized)
            except EmailNotValidError:
                continue
    return list(emails)

def extract_and_validate_contacts(content):
    if not content or not isinstance(content, str):
        return [], []
    
    valid_emails = extract_emails_with_fallbacks(content)
    
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{3,4}'
    extracted_phones = re.findall(phone_pattern, content)
    valid_phones = []
    
    for phone in extracted_phones:
        try:
            parsed = phonenumbers.parse(phone, None)
            if phonenumbers.is_valid_number(parsed):
                valid_phones.append(
                    phonenumbers.format_number(
                        parsed,
                        phonenumbers.PhoneNumberFormat.INTERNATIONAL
                    )
                )
        except phonenumbers.NumberParseException:
            continue
    
    return valid_emails, valid_phones

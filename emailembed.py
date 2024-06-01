import os
import mailbox
import re
from email.utils import parseaddr, parsedate_to_datetime
from email.header import decode_header
from datetime import datetime, timezone

source_dir = 'source/Gmail'
output_dir = 'output'
email_counter = 1

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def decode_mime_words(s):
    if s is None:
        return ""
    decoded_words = decode_header(s)
    decoded_string = ""
    for part in decoded_words:
        if isinstance(part[0], bytes):
            encoding = part[1] or 'utf-8'
            try:
                decoded_string += part[0].decode(encoding)
            except LookupError:
                decoded_string += part[0].decode('utf-8', errors='replace')
        else:
            decoded_string += part[0]
    return decoded_string

def normalize_text(text):
    # Replace consecutive spaces and tabs with a single space
    text = re.sub(r'[ \t]+', ' ', text).strip()
    # Replace sequences of more than two line breaks with exactly two line breaks
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    # Remove parentheses and their content
    text = re.sub(r'\(.*?\)', '', text)
    # Remove standalone brackets and their content
    text = re.sub(r'\[.*?\]', '', text)
    # Remove standalone less-than and greater-than signs
    text = re.sub(r'<.*?>', '', text)
    # Remove any remaining standalone brackets and less-than/greater-than signs
    text = re.sub(r'[\[\]<>]', '', text)
    return text

def format_email(email_id, date, sender, receiver, subject, body):
    return f"""*** MAIL ***
ID: {email_id}
DATE: {date}
SENDER: {sender}
RECEIVER: {receiver}
SUBJECT: {subject}

BODY:
{body}

"""

emails = []

for mbox_file in os.listdir(source_dir):
    if mbox_file.endswith('.mbox'):
        mbox = mailbox.mbox(os.path.join(source_dir, mbox_file))
        for message in mbox:
            date = parsedate_to_datetime(message['date']) if message['date'] else None
            if date and date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)
            sender = decode_mime_words(message['from'])
            receiver = decode_mime_words(message['to'])
            subject = decode_mime_words(message['subject'])
            body = ""
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode(part.get_content_charset(), errors='replace')
                    break

            body = normalize_text(body)
            body = clean_text(body)
            emails.append((date, sender, receiver, subject, body))

# Sort emails by date
emails.sort(key=lambda x: x[0] if x[0] else datetime.min.replace(tzinfo=timezone.utc))

for email in emails:
    date, sender, receiver, subject, body = email
    email_id = f"EMAIL{email_counter:04d}"
    email_counter += 1

    date_str = date.strftime('%b %d, %Y %I:%M %p') if date else "Unknown"
    domain = parseaddr(sender)[1].split('@')[-1] if sender else "unknown_domain"
    output_file = os.path.join(output_dir, f"{domain}.txt")
    email_content = format_email(email_id, date_str, sender, receiver, subject, body)

    with open(output_file, 'a') as f:
        f.write(email_content)

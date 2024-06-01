import os
import mailbox
import re
from email.utils import parseaddr, parsedate_to_datetime
from email.header import decode_header
from datetime import datetime, timezone
from tqdm import tqdm

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

def remove_emails_and_urls(text):
    text = re.sub(r'<[^>]+>', '', text)  # Remove content within angle brackets
    text = re.sub(r'\[https?://[^\]]+\]', '', text)  # Remove content within square brackets with URLs
    return text

def format_email(email_id, date, sender, receiver, subject, body):
    sender = remove_emails_and_urls(sender).replace('"', '')
    receiver = remove_emails_and_urls(receiver).replace('"', '')
    body = remove_emails_and_urls(body)
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

mbox_files = [f for f in os.listdir(source_dir) if f.endswith('.mbox')]

for mbox_file in tqdm(mbox_files, desc="Processing mbox files"):
    mbox = mailbox.mbox(os.path.join(source_dir, mbox_file))
    for message in tqdm(mbox, desc=f"Processing emails in {mbox_file}", leave=False):
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

        emails.append((date, sender, receiver, subject, body))

# Sort emails by date
emails.sort(key=lambda x: x[0] if x[0] else datetime.min.replace(tzinfo=timezone.utc))

for email in tqdm(emails, desc="Writing emails to files"):
    date, sender, receiver, subject, body = email
    email_id = f"EMAIL{email_counter:04d}"
    email_counter += 1

    date_str = date.strftime('%b %d, %Y %I:%M %p') if date else "Unknown"
    domain = parseaddr(sender)[1].split('@')[-1] if sender else "unknown_domain"
    output_file = os.path.join(output_dir, f"{domain}.txt")
    email_content = format_email(email_id, date_str, sender, receiver, subject, body)

    with open(output_file, 'a') as f:
        f.write(email_content)

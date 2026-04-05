import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

# --- SETTINGS ---
URL = "https://reslife.brown.edu/housing-selection/selection-resources"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") 
STATE_FILE = "last_link.txt"
ALL_LINKS_FILE = "all_links.txt"
PDF_OUTPUT_DIR = "liveDataPDFs"

def send_ping(message):
    """Sends a push notification to Slack."""
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"text": message})

def main():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pdf_link = None
    for a in soup.find_all('a', href=True):
        if '.pdf' in a['href'].lower():
            pdf_link = a['href']
            if not pdf_link.startswith('http'):
                pdf_link = "https://reslife.brown.edu" + pdf_link
            break
            
    if not pdf_link:
        print("Could not find a PDF on the page.")
        return

    old_link = ""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            old_link = f.read().strip()

    if pdf_link == old_link:
        print("No changes. The PDF is the same.")
        return

    print(f"New PDF found: {pdf_link}")
    pdf_resp = requests.get(pdf_link)

    os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    source_pdf_name = os.path.basename(pdf_link.split("?")[0])
    pdf_filename = os.path.join(PDF_OUTPUT_DIR, f"housing_data_{timestamp}_{source_pdf_name}")
    
    with open(pdf_filename, 'wb') as f:
        f.write(pdf_resp.content)

    print(f"Saved PDF as: {pdf_filename}")

    if old_link:
        with open(ALL_LINKS_FILE, 'a') as f:
            f.write(old_link + "\n")
        
    with open(STATE_FILE, 'w') as f:
        f.write(pdf_link)

    send_ping(f"<!channel> HOUSING SPREADSHEET UPDATED. New PDF: {pdf_link}")

if __name__ == "__main__":
    main()
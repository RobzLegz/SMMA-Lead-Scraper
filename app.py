import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time
import csv

# Function to extract emails from a text using regex
def extract_emails(text):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    return list(set(re.findall(email_regex, text)))

def extract_facebook_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    facebook_links = set()

    # Extract Facebook URLs from meta tags
    for meta_tag in soup.find_all('meta', {'property': 'og:url'}):
        content = meta_tag.get('content', '')
        if 'facebook.com' in content:
            facebook_links.add(content)

    # Extract Facebook URLs from anchor tags
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if 'facebook.com' in href:
            facebook_links.add(href)

    return list(facebook_links)

# Function to extract LinkedIn URLs from HTML content
def extract_linkedin_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    linkedin_links = set()

    # Extract LinkedIn URLs from meta tags
    for meta_tag in soup.find_all('meta', {'property': 'og:url'}):
        content = meta_tag.get('content', '')
        if 'linkedin.com' in content:
            linkedin_links.add(content)

    # Extract LinkedIn URLs from anchor tags
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if 'linkedin.com' in href:
            linkedin_links.add(href)

    return list(linkedin_links)

data = []

country = input("Enter country: ")
service = input("Enter service / niche: ")

# Load the CSV file into a DataFrame
df = pd.read_csv('scraped_leads.csv')

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    try:
        website = row['Website']
        business_name = row['Business Name']
        address = row['Address']
        phone = row['Phone'].replace(" ", "")

        # Fetch the webpage content
        response = requests.get(website)
        html_content = response.text

        # Extract and print emails from the webpage content
        emails = extract_emails(html_content)
        facebook_urls = extract_facebook_urls(html_content)
        linkedin_urls = extract_linkedin_urls(html_content)

        d = {
            "website": website,
            "business_name": business_name,
            "address": address,
            "phone": phone,
            "work_email": "",
            "other_email": "",
            "home_email": "",
            "facebook_url": "",
            "linkedin_url": "",
        }

        if emails:
            if len(emails) > 0:
                d["work_email"] = emails[0]
                if len(emails) > 1:
                    d["other_email"] = emails[1]
                    if len(emails) > 2:
                        d["home_email"] = emails[2]

            print(f"Unique emails found for {business_name} ({website}): {', '.join(emails)}")

        if facebook_urls:
            if len(facebook_urls) > 0:
                d["facebook_url"] = facebook_urls[0]

            print(f"Facebook URLs found for {business_name} ({website}): {', '.join(facebook_urls)}")

        if linkedin_urls:
            if len(linkedin_urls) > 0:
                d["linkedin_url"] = linkedin_urls[0]
            
            print(f"LinkedIn URLs found for {business_name} ({website}): {', '.join(linkedin_urls)}")

        if not (emails or facebook_urls or linkedin_urls):
            print(f"No relevant information found for {business_name}")
            time.sleep(1.5)
            continue

        data.append(d)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {website}: {e}")

    time.sleep(1.5)


csv_file_path = 'leads_out.csv'
header = [
    "ID", "Lead Name", "Salutation", "First Name", "Last Name", "Middle Name", "First And Last Names",
    "Date of birth", "Address", "Street, house no.", "Apartment, office, room, floor", "City", "District",
    "Region/Area", "Zip/Postal code", "Country", "Work Phone", "Mobile", "Fax", "Home Phone", "Pager Number",
    "SMS marketing phone", "Other Phone Number", "Corporate Website", "Personal Page", "Facebook Page",
    "VK Page", "LiveJournal", "Twitter", "Other Website", "Work E-mail", "Home E-mail", "Newsletters email",
    "Other E-mail", "Facebook account", "Telegram account", "VK account", "Skype ID", "Viber contact",
    "Instagram comments", "Network contact", "Live Chat", "Open Channel account", "ICQ Number", "MSN/Live!",
    "Jabber", "Other Contact", "Linked user", "Company Name", "Position", "Comment", "Stage", "More about this stage",
    "Product", "Price", "Quantity", "Opportunity", "Currency", "Source", "Source information", "Available to everyone",
    "Responsible person", "Type of service", "Language", "Bitrix24 User", "Opener", "Cookie Consent",
    "Advertising budget", "Information about the advertised product", "Customer need", "Comment on a lost deal"
]

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=';')
    
    csv_writer.writeheader()

    for idx, lead in enumerate(data, start=1):
        csv_writer.writerow({
            "ID": idx,
            "Corporate Website": lead.get("website", ""),
            "Company Name": lead.get("business_name", ""),
            "Lead Name": lead.get("business_name", ""),
            "Address": lead.get("address", ""),
            "Work Phone": lead.get("phone", ""),
            "Work E-mail": lead.get("work_email", ""),
            "Other E-mail": lead.get("other_email", ""),
            "Home E-mail": lead.get("home_email", ""),
            "Facebook Page": lead.get("facebook_url", ""),
            "Other Website": lead.get("linkedin_url", ""),
            "Country": country,
            "Comment": "Data miner google maps",
            "Opportunity": 1000,
            "Currency": "EUR",
            "Available to everyone": "no",
            "Product": service
        })

print(f"CSV file '{csv_file_path}' has been created.")


csv_file_path = 'sheets_leads.csv'
header = [
    "Business Name", "Address", "Phone", "Website", "Email", "Email 2", "Email 3", "Facebook", "Linkedin", "Notes", "Contacted"
]

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=';')
    
    csv_writer.writeheader()

    for idx, lead in enumerate(data, start=1):
        csv_writer.writerow({
            "Business Name": lead.get("business_name", ""),
            "Website": lead.get("website", ""),
            "Address": lead.get("address", ""),
            "Phone": lead.get("phone", ""),
            "Email": lead.get("work_email", ""),
            "Email 2": lead.get("other_email", ""),  
            "Email 3": lead.get("home_email", ""),
            "Facebook": lead.get("facebook_url", ""),
            "Linkedin": lead.get("linkedin_url", ""),
            "Notes": "Data miner google maps",
            "Contacted": "",
        })

print(f"CSV file '{csv_file_path}' has been created.")

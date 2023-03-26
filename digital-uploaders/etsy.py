import json
import os

import requests

# Define your credentials
API_KEY = os.getenv('ETSY_API_KEY')
SHARED_SECRET = os.getenv('ETSY_SHARED_SECRET')
ACCESS_TOKEN = os.getenv('ETSY_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ETSY_ACCESS_TOKEN_SECRET')
FLORAL_PATTERN_ZIP = os.getenv('FLORAL_PATTERN_ZIP')

# Define your endpoint
url = "https://openapi.etsy.com/v2/listings"

# Define your headers
headers = {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY,
    "X-SHARED-SECRET": SHARED_SECRET,
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}

# Define your payload
payload = {
    "title": "Floral Pattern Images",
    "description": "A collection of high-quality floral pattern images.",
    "price": 10.0,
    "quantity": 1,
    "materials": ["zip file"],
    "shipping_template_id": 123456789,
    "who_made": "i_did",
    "when_made": "2023_2024",
    "is_supply": True,
}

# Define your files
files = {
    'zipfile': ('floral_patterns.zip', open(FLORAL_PATTERN_ZIP, 'rb')),
    'image1': ('image1.jpg', open('image1.jpg', 'rb')),
    'image2': ('image2.jpg', open('image2.jpg', 'rb')),
}

# Send the request
response = requests.post(url, headers=headers, data=json.dumps(payload), files=files)

# Print the response
print(response.json())

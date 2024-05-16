import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def clean_text(text):
    replacements = {
        '\n': '',
        '\u2014': '',
        '\u2019': '',
        '\n\n': '',
        '\u201c': '',
        '#': ' #',
        'https': ' https',
        '\u201d': ' '
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def export_json_from_endpoint(endpoint_url, results_dir, filename):
    max_retries = 3
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(endpoint_url)
            
            if response.status_code == 200:
                data = response.json()

                # Clean the text in the "post" field
                for item in data:
                    if 'post' in item:
                        item['post'] = clean_text(item['post'])
                
                os.makedirs(results_dir, exist_ok=True)
                filepath = os.path.join(results_dir, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=4)
                
                print(f"Successfully exported JSON data to {filepath}")
                return
            else:
                print(f"Error: {response.status_code} - {response.text}")
        
        except requests.RequestException as e:
            print(f"Request failed: {str(e)}")
        
        print(f"Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)
    
    print("Failed to fetch data after multiple attempts.")

if __name__ == "__main__":
    endpoint_url = os.getenv("ENDPOINT_URL")
    results_dir = "results"
    filename = "results.json"
    
    if endpoint_url is None:
        print("ENDPOINT_URL not found in .env file.")
    else:
        export_json_from_endpoint(endpoint_url, results_dir, filename)

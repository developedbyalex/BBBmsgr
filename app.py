import requests
import json
import time
from colorama import init, Fore, Style
import itertools
import sys
import os

# Function to clear console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to load config
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

# Clear console at the start
clear_console()

# ASCII art banner
banner = '''
 ____  ____  ____  __  __                
| __ )| __ )| __ )|  \/  |___  __ _ _ __ 
|  _ \|  _ \|  _ \| |\/| / __|/ _` | '__|
| |_) | |_) | |_) | |  | \__ \ (_| | |   
|____/|____/|____/|_|  |_|___/\__, |_|   
                              |___/      
'''

# Display banner and creator info
print(Fore.CYAN + banner + Style.RESET_ALL)
print(Fore.MAGENTA + "Made By Lofi (https://builtbybit.com/members/lofi.34798/)" + Style.RESET_ALL)
print("\n" + "=" * 50 + "\n")

# Initialize colorama
init()

# Load config
config = load_config()
API_TOKEN = config['API_TOKEN']
RESOURCE_ID = config['RESOURCE_ID']
MESSAGE_TITLE = config['MESSAGE_TITLE']
MESSAGE_CONTENTS = config['MESSAGE_CONTENTS']

# API base URL
BASE_URL = "https://api.builtbybit.com/v1"

# Headers for authentication
headers = {
    "Authorization": f"Private {API_TOKEN}",
    "Content-Type": "application/json"
}

def check_api_connection():
    url = f"{BASE_URL}/health"
    try:
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except:
        return False

def get_resource_info(resource_id):
    url = f"{BASE_URL}/resources/{resource_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()["data"]
        return data["title"], data["purchase_count"]
    return "Unknown Resource", 0

def get_purchases(resource_id):
    url = f"{BASE_URL}/resources/{resource_id}/purchases"
    params = {
        "sort": "purchase_date",
        "order": "desc",
        "page": 1
    }
    
    purchases = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()["data"]
            if not data:
                break
            purchases.extend(data)
            params["page"] += 1
        else:
            break
        time.sleep(1)  # Cooldown to avoid rate limiting
    return purchases

def check_user_status(user_id):
    url = f"{BASE_URL}/members/{user_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()["data"]
        return user_data.get("suspended", False), user_data.get("banned", False), user_data.get("username", "Unknown")
    return None, None, "Unknown"

def animated_loading():
    for c in itertools.cycle(['\\', '|', '/', '-']):
        yield c

def send_message(user_id, username):
    url = f"{BASE_URL}/conversations"
    data = {
        "recipient_ids": [user_id],
        "title": MESSAGE_TITLE,
        "message": MESSAGE_CONTENTS
    }
    
    loading = animated_loading()
    for _ in range(10):  # Show loading animation
        sys.stdout.write(f"\rMessaging {username} {next(loading)}")
        sys.stdout.flush()
        time.sleep(0.1)
    
    response = requests.post(url, headers=headers, json=data)
    sys.stdout.write("\r" + " " * 50 + "\r")  # Clear the line
    
    if response.status_code == 200:
        print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Message sent to {username} successfully.")
        return True
    else:
        print(f"{Fore.RED}[✗]{Style.RESET_ALL} Failed to send message to {username}. Status code: {response.status_code}")
        return False

# Main execution
print("BuiltByBit API:", end=" ")
if check_api_connection():
    print(f"{Fore.GREEN}Connected{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}Offline{Style.RESET_ALL}")
    sys.exit(1)

resource_name, purchase_count = get_resource_info(RESOURCE_ID)
purchases = get_purchases(RESOURCE_ID)
suspended_count = 0
banned_count = 0
messaged_users = set()

print(f"\nFound {purchase_count} purchases for {resource_name}.")

for purchase in purchases:
    is_suspended, is_banned, username = check_user_status(purchase["purchaser_id"])
    
    if is_suspended:
        print(f"{Fore.YELLOW}[⚠️] {username} is suspended. Skipping them to save on the rate limit.{Style.RESET_ALL}")
        suspended_count += 1
        continue
    
    if is_banned:
        print(f"{Fore.RED}[🚫] {username} is banned. Skipping them.{Style.RESET_ALL}")
        banned_count += 1
        continue
    
    if username in messaged_users:
        print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} Skipping duplicate user: {username}")
        continue
    
    if send_message(purchase["purchaser_id"], username):
        messaged_users.add(username)
    
    time.sleep(2)  # Cooldown between messages to avoid rate limiting

print(f"\nMessaging complete. ({suspended_count} users suspended, {banned_count} users banned, {len(messaged_users)} unique users messaged)")

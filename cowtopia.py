import requests
import time
import json


def read_query_data(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def authenticate(query_data):
    url = "https://cowtopia-be.tonfarmer.com/auth"
    
    headers = {
        "Content-Type": "application/json",
        "X-Tg-Data": query_data,
    }

    response = requests.post(url, headers=headers, json={})
    
    if response.status_code == 201:
        data = response.json()
        access_token = data.get("data", {}).get("access_token")
        
        if access_token:
            username = data["data"]["user"]["username"]
            print(f"Authentication successful! Username: {username}")
            print("Response data:", json.dumps(data, indent=4))
            return access_token
        else:
            print("Authentication failed: Access token not found.")
            return None
    else:
        print("Failed to authenticate:", response.status_code, response.text)
        return None

def clear_tasks(access_token):
    groups = ["partner", "main"]
    for group in groups:
        url = f"https://cowtopia-be.tonfarmer.com/mission?group={group}"
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {access_token}",
            "Origin": "https://cowtopia-prod.tonfarmer.com",
            "Referer": "https://cowtopia-prod.tonfarmer.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
            "X-Chain-Id": "43113",
            "X-Lang": "en",
            "X-OS": "miniapp",
        }

        response = requests.get(url, headers=headers)  # Changed to GET

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"Tasks cleared successfully for group '{group}'!")
                print("Response data:", json.dumps(data, indent=4))
                return data  # Return data for further processing
            else:
                print(f"Failed to clear tasks for group '{group}':", data.get("message"))
        else:
            print(f"Failed to clear tasks for group '{group}':", response.status_code, response.text)

def get_game_info(access_token):
    url = "https://cowtopia-be.tonfarmer.com/user/game-info"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {access_token}",
        "Origin": "https://cowtopia-prod.tonfarmer.com",
        "Referer": "https://cowtopia-prod.tonfarmer.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        "X-Chain-Id": "43113",
        "X-Lang": "en",
        "X-OS": "miniapp",
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        game_info = response.json().get('data', {})
        user_info = game_info.get('user', {})
        
        token = user_info.get('token', 'N/A')
        money = user_info.get('money', 'N/A')
        username = user_info.get('username', 'N/A')
        
        print(f'"token": {token}, "money": {money}, "username": "{username}"')
    else:
        print("Failed to retrieve game info:", response.status_code, response.text)

        
def complete_tasks(missions):
    for mission in missions:
        if not mission['completed'] and mission['url']:
            response = requests.get(mission['url'])
            if response.status_code == 200:
                print(f"Completed task: {mission['name']}")
                # Optionally update task status in your backend here
            else:
                print(f"Failed to complete task: {mission['name']}")


def check_offline_profit(access_token):
    url = "https://cowtopia-be.tonfarmer.com/user/offline-profit"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {access_token}",
        "Origin": "https://cowtopia-prod.tonfarmer.com",
        "Referer": "https://cowtopia-prod.tonfarmer.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        "X-Chain-Id": "43113",
        "X-Lang": "en",
        "X-OS": "miniapp",
    }

    while True:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("Response data:", json.dumps(data, indent=4))
            time_diff = data['data']['time_diff']
            print(f"Time difference: {time_diff} seconds")
            # After checking offline profit, update game info
            get_game_info(access_token)
        else:
            print("Failed to retrieve offline profit:", response.status_code, response.text)
        
        # Wait for 30 seconds
        time.sleep(30)       

def main():
    tg_data = read_query_data("query.txt")
    access_token = authenticate(tg_data)

    if access_token:
        # Clear tasks and retrieve missions data
        response_data = clear_tasks(access_token)
        if response_data:
            # Complete tasks using the fetched missions data
            complete_tasks(response_data['data']['missions'])
            # Get game info after completing tasks
            get_game_info(access_token)
            check_offline_profit(access_token)

if __name__ == "__main__":
    main()
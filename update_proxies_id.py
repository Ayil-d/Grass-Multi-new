import random
import requests
import os
import logging

def setup_logging():
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='update_proxies.log', level=logging.ERROR, format=log_format)

def update_proxies_and_user_id():
    # Download proxies from api
    proxies_url = "https://api.s5proxies.com/api2.php?do=download&key=65fcb18e928802024032105154265fcb18e9288e&is_type="
    response = requests.get(proxies_url)
    lines = response.text.strip().split('\n')
    
    # Add "socks5://" prefix to each proxy and skip the header line
    proxies = [f"socks5://{line.split(',')[0]}" for line in lines[1:] if line.strip()]

    # Limit proxies to 1500 - you can increase or reduce if you like
    proxies = proxies[:1500]

    # Get the absolute path to the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the absolute path to user_ids.txt
    user_ids_path = os.path.join(script_dir, "user_ids.txt")

    # Check if the user_ids.txt file exists
    if not os.path.exists(user_ids_path):
        error_msg = f"Error: File '{user_ids_path}' does not exist."
        logging.error(error_msg)
        print(error_msg)
        return

    # Update socks5_proxies.txt
    socks5_proxies_path = os.path.join(script_dir, "socks5_proxies.txt")
    with open(socks5_proxies_path, "w") as f:
        f.write("\n".join(proxies))

    # Read user IDs from user_ids.txt
    with open(user_ids_path, "r") as user_ids_file:
        user_ids = [line.strip() for line in user_ids_file]
        if not user_ids:
            error_msg = f"Error: No user IDs found in '{user_ids_path}'."
            logging.error(error_msg)
            print(error_msg)
            return
        selected_user_id = random.choice(user_ids)

    # Update user_id.txt
    user_id_path = os.path.join(script_dir, "user_id.txt")
    with open(user_id_path, "w") as user_id_file:
        user_id_file.write(selected_user_id)

if __name__ == "__main__":
    setup_logging()
    update_proxies_and_user_id()

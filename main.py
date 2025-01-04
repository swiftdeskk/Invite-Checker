import requests
import os
import yaml
import time
import fade
import random
import threading
import ctypes
from colorama import Fore, init
from datetime import datetime
from pystyle import Center

init(autoreset=True)

total_invites = 0
valid_invites = 0
bad_invites = 0
invalid_invites = 0
rate_limits = 0
start_time = time.time()

GUI = """
██╗███╗░░██╗██╗░░░██╗██╗████████╗███████╗  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
██║████╗░██║██║░░░██║██║╚══██╔══╝██╔════╝  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
██║██╔██╗██║╚██╗░██╔╝██║░░░██║░░░█████╗░░  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
██║██║╚████║░╚████╔╝░██║░░░██║░░░██╔══╝░░  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
██║██║░╚███║░░╚██╔╝░░██║░░░██║░░░███████╗  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░░╚═╝░░░╚══════╝  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
"""
FADED_GUI = fade.purplepink(Center.XCenter(GUI))
class Log:
    @staticmethod
    def _log(prefix, message):
        current_time = datetime.now().strftime("%H:%M %p")
        print(f"{Fore.LIGHTBLACK_EX}{current_time} {prefix}{message}")

    @staticmethod
    def Success(message, prefix=f"SCS : {Fore.RESET}", color=Fore.LIGHTGREEN_EX):
        Log._log("", f"{color}{prefix}{message}{Fore.RESET}")

    @staticmethod
    def Error(message, prefix=f"WRN : {Fore.RESET}", color=Fore.RED):
        Log._log("", f"{color}{prefix}{message}{Fore.RESET}")

    @staticmethod
    def Info(message, prefix=f"INF : {Fore.RESET}", color=Fore.LIGHTCYAN_EX):
        Log._log("", f"{color}{prefix}{message}{Fore.RESET}")

    @staticmethod
    def Warning(message, prefix=f"BAD : {Fore.RESET}", color=Fore.LIGHTRED_EX):
        Log._log("", f"{color}{prefix}{message}{Fore.RESET}")

def load_file(filepath):
    try:
        with open(filepath, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        Log.Error(f"The file {Fore.LIGHTBLACK_EX}{filepath}{Fore.RESET} was not found.")
        return []

def parse_invite(invite):
    if invite.startswith("https://discord.gg/"):
        return invite.split("https://discord.gg/")[1]
    return invite

def fetch_invite_details(invite_code, proxy=None):
    url = f"https://discord.com/api/v10/invites/{invite_code}?with_counts=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    } if proxy else None

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "server_name": data.get("guild", {}).get("name", "Unknown"),
                "member_count": data.get("approximate_member_count", 0),
                "online_count": data.get("approximate_presence_count", 0),
                "boosts": data.get("guild", {}).get("premium_subscription_count", 0),
            }
        elif response.status_code == 404:
            return {"error": "Invalid invite code."}
        else:
            return {"error": f"Failed to fetch details. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def save_to_file(directory, filename, content):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, "a") as file:
        file.write(content + "\n")

def display_details(invite_code, details, config):
    global valid_invites, bad_invites, invalid_invites, rate_limits
    if "error" in details:
        if "rate limit" in details["error"].lower():
            rate_limits += 1
        elif "invalid" in details["error"].lower():
            invalid_invites += 1
        else:
            bad_invites += 1
        Log.Error(f"Invite: {Fore.LIGHTBLACK_EX}{invite_code}{Fore.RESET}, Error: {Fore.LIGHTBLACK_EX}{details['error']}{Fore.RESET}")
        save_to_file(config["output_directory"], "failed.txt", f"https://discord.gg/{invite_code} | {details['error']}")
    else:
        if details["member_count"] >= config["min_members"]:
            valid_invites += 1
            Log.Success(f"Invite: {Fore.LIGHTBLACK_EX}{invite_code}{Fore.RESET}, Server Name: {Fore.LIGHTBLACK_EX}{details['server_name']}{Fore.RESET}, Total Members: {Fore.LIGHTBLACK_EX}{details['member_count']}{Fore.RESET}, Active Members: {Fore.LIGHTBLACK_EX}{details['online_count']}{Fore.RESET}, Boosts: {Fore.LIGHTBLACK_EX}{details['boosts']}")
            save_to_file(config["output_directory"], "success.txt", f"https://discord.gg/{invite_code}")
        else:
            bad_invites += 1
            Log.Warning(f"Invite: {Fore.LIGHTBLACK_EX}{invite_code}{Fore.RESET}, Server Name: {Fore.LIGHTBLACK_EX}{details['server_name']}{Fore.RESET}, Total Members: {Fore.LIGHTBLACK_EX}{details['member_count']}{Fore.RESET}, Active Members: {Fore.LIGHTBLACK_EX}{details['online_count']}{Fore.RESET}, Boosts: {Fore.LIGHTBLACK_EX}{details['boosts']}")
            save_to_file(config["output_directory"], "bad.txt", f"https://discord.gg/{invite_code}")
    update_console_title()

def update_console_title():
    elapsed_time = time.time() - start_time
    title = (f"Invite Checker | discord.gg/moonlygg | Moonlygg.com | Total: {total_invites} | Valid: {valid_invites} | "
             f"Bad: {bad_invites} | Invalid: {invalid_invites} | RateLimit: {rate_limits} | "
             f"Elapsed Time: {elapsed_time:.8f}s")
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def process_invite(invite, proxies, config):
    invite_code = parse_invite(invite)
    proxy = random.choice(proxies) if proxies and config["use_proxies"] else None
    details = fetch_invite_details(invite_code, proxy)
    display_details(invite_code, details, config)


def main():
    global total_invites

    with open("config.yaml", "r") as yaml_file:
        config = yaml.safe_load(yaml_file)["invite_checker"]

    invites = load_file(config["invites_file"])
    proxies = load_file(config["proxies_file"]) if config["use_proxies"] else []

    if not invites:
        Log.Warning("No invitations were found.")
        return
    print(FADED_GUI)
    Log.Success("Welcome to Moonly Invite Checker\n")
    Log.Info(f"Invites -> {Fore.LIGHTBLACK_EX}{len(invites)}{Fore.RESET}")
    proxies_status = "Enabled" if config["use_proxies"] else "Disabled"
    Log.Info(f"Proxies -> {Fore.LIGHTBLACK_EX}{proxies_status}{Fore.RESET}")
    min_members = config["min_members"]
    Log.Info(f"Min Members -> {Fore.LIGHTBLACK_EX}{min_members}{Fore.RESET}\n")
    total_invites = len(invites)
    update_console_title()

    timestamp = datetime.now().strftime("%d-%m-%y %H-%M-%S")
    config["output_directory"] = os.path.join(config["output_directory"], timestamp)

    threads = []

    for invite in invites:
        thread = threading.Thread(target=process_invite, args=(invite, proxies, config))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print()
    Log.Info("Press Enter to close the program.")
    input()

if __name__ == "__main__":
    main()
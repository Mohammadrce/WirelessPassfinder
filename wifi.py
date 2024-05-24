import subprocess
import re
import os
from colorama import Fore, init
import time

def get_wifi_profiles():
    result = subprocess.run(['netsh','wlan','show','profiles'],capture_output=True,text=True)
    profiles = re.findall(r"All User Profile\s*:\s*(.*)",result.stdout)
    return [profile.strip() for profile in profiles]

def get_wifi_password(profile):
    """Retrieve the WiFi password for a given profile name."""
    result = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"], capture_output=True, text=True)
    password_match = re.search(r"Key Content\s*:\s*(.*)", result.stdout)
    return password_match.group(1).strip() if password_match else None

def main():
    init(autoreset=True)
    
    print(Fore.CYAN + "Starting ...")
    time.sleep(1)
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    
    print(Fore.GREEN + "Fetching WiFi passwords ...\n")
    wifi_profiles = get_wifi_profiles()
    
    for profile in wifi_profiles:
        password = get_wifi_password(profile)
        if password:
            print(f"{Fore.GREEN}WiFi: {profile} - Password: {password}")
        else:
            print(f"{Fore.RED}WiFi: {profile} - Password: Not found")
    
    print(Fore.GREEN + "Done.")

if __name__ == "__main__":
    main()

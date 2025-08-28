import subprocess
import os
import re
import getpass
#administrative privileges are required to run this script

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        
        subprocess.check_call('net session', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def get_temp_path():
    """Get the path to the user's Temp directory."""
    username = getpass.getuser()
    temp_path = os.path.join(f"C:\\Users\\{username}\\AppData\\Local\\Temp", "temp.txt")
    return temp_path


def get_wifi_profiles():
    """Retrieve a list of all Wi-Fi profiles stored on the system."""
    try:
        # netsh command 
        result = subprocess.run(
            'netsh wlan show profiles',
            capture_output=True,
            text=True,
            shell=True
        )
        output = result.stdout
        #  profile names 
        profiles = re.findall(r"All User Profile\s+:\s+(.+)", output)
        return profiles
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Wi-Fi profiles: {e}")
        return []

def get_wifi_password(profile_name):
    """Retrieve the password for a specific Wi-Fi profile."""
    try:
        # netsh command again 
        result = subprocess.run(
            f'netsh wlan show profile name="{profile_name}" key=clear',
            capture_output=True,
            text=True,
            shell=True
        )
        output = result.stdout
        # Extracting the password
        match = re.search(r"Key Content\s+:\s+(.+)", output)
        if match:
            return match.group(1)
        else:
            return "No password found or not available"
    except subprocess.CalledProcessError as e:
        return f"Error retrieving password: {e}"

def main():
    """Main function to extract Wi-Fi passwords and save them to a file."""
    print("Extracting Wi-Fi passwords...")

    # admin privileges
    if not is_admin():
        print("This script requires administrative privileges to access Wi-Fi passwords.")
        print("Please run this script as an Administrator.")
        input("Press Enter to exit...")
        return

    # output file path
    output_file = get_temp_path()
    
    # All Wi-Fi profiles
    profiles = get_wifi_profiles()
    
    if not profiles:
        print("No Wi-Fi profiles found or an error occurred.")
        input("Press Enter to exit...")
        return
    
    # Opening the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Wi-Fi Passwords Report\n")
            f.write("=" * 50 + "\n\n")
            
            # Arranging profiles and passwords
            for profile in profiles:
                password = get_wifi_password(profile)
                f.write(f"Wi-Fi SSID: {profile}\n")
                f.write(f"Password: {password}\n")
                f.write("-" * 50 + "\n")
                print(f"Processed: {profile}")
                
        print(f"\nWi-Fi passwords have been saved to: {output_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()

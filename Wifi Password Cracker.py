import subprocess

def get_wifi_profiles():
    meta_data_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
    meta_data_str = meta_data_output.decode('utf-8', errors="backslashreplace")
    data = meta_data_str.split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    return profiles

def get_wifi_password(profile):
    try:
        results_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'])
        results_str = results_output.decode('utf-8', errors="backslashreplace")
        results = [b.split(":")[1][1:-1] for b in results_str.split('\n') if "Key Content" in b]
        return results[0] if results else ""
    except subprocess.CalledProcessError:
        return "Encoding Error Occurred"

def main():
    wifi_profiles = get_wifi_profiles()

    print("{:<30}| {:<30} | {:<20}".format("Wi-Fi Name", "Password", "Nearby Network"))
    print("-" * 80)

    for profile in wifi_profiles:
        password = get_wifi_password(profile)
        nearby_flag = profile in subprocess.check_output(['netsh', 'wlan', 'show', 'network']).decode('ascii').replace("\r", "").split('\n')

        print("{:<30}| {:<30} | {:<20}".format(profile, password, "Y" if nearby_flag else "N"))

if __name__ == "__main__":
    main()

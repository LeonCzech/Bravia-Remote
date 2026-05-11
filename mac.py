import requests
import json
import sys
import tty
import termios

# Mapping codes extracted from your specific Bravia model
IRCC_MAP = {
    'w': 'AAAAAQAAAAEAAAB0Aw==', # Up
    's': 'AAAAAQAAAAEAAAB1Aw==', # Down
    'a': 'AAAAAQAAAAEAAAA0Aw==', # Left
    'd': 'AAAAAQAAAAEAAAAzAw==', # Right
    'f': 'AAAAAQAAAAEAAABlAw==', # Confirm/OK
    'b': 'AAAAAgAAAJcAAAAjAw==', # Return/Back
    'h': 'AAAAAQAAAAEAAABgAw==', # Home
    'v': 'AAAAAQAAAAEAAAATAw==', # VolumeDown
    'V': 'AAAAAQAAAAEAAAASAw==', # VolumeUp
    'p': 'AAAAAQAAAAEAAAAVAw=='  # Power Toggle
}

def send_ircc(tv_ip, psk, code):
    url = f"http://{tv_ip}/sony/ircc"
    headers = {
        "X-Auth-PSK": psk,
        "Content-Type": "text/xml; charset=UTF-8",
        "SOAPACTION": '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"'
    }
    data = f'<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1"><IRCCCode>{code}</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>'
    try:
        requests.post(url, data=data, headers=headers, timeout=0.5)
    except:
        pass

def remote_loop(tv_ip, psk):
    print("\n" + "="*45)
    print(f"  SONY REMOTE SESSION: {tv_ip}")
    print("="*45)
    print(" [W] Up          [F] OK / Confirm")
    print(" [S] Down        [B] Back / Return")
    print(" [A] Left        [H] Home Menu")
    print(" [D] Right       [Q] Quit Script")
    print("-" * 45)
    print(" [v] Vol Down    [V] Vol Up (Shift+V)")
    print(" [p] Power Toggle")
    print("="*45)

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            char = sys.stdin.read(1)
            if char.lower() == 'q': 
                break
            if char in IRCC_MAP:
                send_ircc(tv_ip, psk, IRCC_MAP[char])
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    print(f"\n[!] Session for {tv_ip} closed.")

if __name__ == "__main__":
    # Ask for credentials at runtime
    print("--- Sony Bravia Connection ---")
    target_ip = input("Enter TV IP (e.g. 192.168.2.31): ").strip()
    target_psk = input("Enter Pre-Shared Key (PSK): ").strip()

    try:
        # Verify connection before starting loop
        url = f"http://{target_ip}/sony/system"
        payload = {"method": "getPowerStatus", "params": [], "id": 1, "version": "1.0"}
        headers = {"X-Auth-PSK": target_psk}
        
        test = requests.post(url, json=payload, headers=headers, timeout=3)
        
        if test.status_code == 200:
            remote_loop(target_ip, target_psk)
        else:
            print(f"\n[!] Auth failed (Status {test.status_code}). Check your PSK.")
    except Exception as e:
        print(f"\n[!] Connection Error: {e}")

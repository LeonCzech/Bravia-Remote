import requests
import json
import sys
import msvcrt  # Windows-specific library for keypresses

# Mapping codes matched to your specific Bravia model
IRCC_MAP = {
    b'w': 'AAAAAQAAAAEAAAB0Aw==', # Up
    b's': 'AAAAAQAAAAEAAAB1Aw==', # Down
    b'a': 'AAAAAQAAAAEAAAA0Aw==', # Left
    b'd': 'AAAAAQAAAAEAAAAzAw==', # Right
    b'f': 'AAAAAQAAAAEAAABlAw==', # Confirm/OK
    b'b': 'AAAAAgAAAJcAAAAjAw==', # Return/Back
    b'h': 'AAAAAQAAAAEAAABgAw==', # Home
    b'v': 'AAAAAQAAAAEAAAATAw==', # VolumeDown
    b'V': 'AAAAAQAAAAEAAAASAw==', # VolumeUp
    b'p': 'AAAAAQAAAAEAAAAVAw=='  # Power Toggle
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
    print("Press a key to control the TV...")

    while True:
        # msvcrt.getch() reads a byte string on Windows
        char = msvcrt.getch()
        
        if char.lower() == b'q':
            break
            
        if char in IRCC_MAP:
            send_ircc(tv_ip, psk, IRCC_MAP[char])

    print(f"\n[!] Session for {tv_ip} closed.")

if __name__ == "__main__":
    print("--- Sony Bravia Connection (Windows) ---")
    target_ip = input("Enter TV IP: ").strip()
    target_psk = input("Enter PSK: ").strip()

    try:
        url = f"http://{target_ip}/sony/system"
        payload = {"method": "getPowerStatus", "params": [], "id": 1, "version": "1.0"}
        headers = {"X-Auth-PSK": target_psk}
        
        test = requests.post(url, json=payload, headers=headers, timeout=3)
        
        if test.status_code == 200:
            remote_loop(target_ip, target_psk)
        else:
            print(f"\n[!] Auth failed. Status: {test.status_code}")
    except Exception as e:
        print(f"\n[!] Connection Error: {e}")

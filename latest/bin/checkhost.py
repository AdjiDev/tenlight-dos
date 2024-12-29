import sys
import time
import requests
from rich.console import Console
from rich.table import Table

node_to_region = {
    'ae1': 'United Arab Emirates',
    'bg1': 'Bulgaria',
    'br1': 'Brazil',
    'ch1': 'Switzerland',
    'cz1': 'Czech Republic',
    'de1': 'Germany',
    'de4': 'Germany',
    'es1': 'Spain',
    'fi1': 'Finland',
    'fr2': 'France',
    'hk1': 'Hong Kong',
    'hr1': 'Croatia',
    'il1': 'Israel',
    'il2': 'Israel',
    'in1': 'India',
    'ir1': 'Iran',
    'ir3': 'Iran',
    'ir5': 'Iran',
    'it2': 'Italy',
    'jp1': 'Japan',
    'kz1': 'Kazakhstan',
    'lt1': 'Lithuania',
    'md1': 'Moldova',
    'nl1': 'Netherlands',
    'nl2': 'Netherlands',
    'pl1': 'Poland',
    'pl2': 'Poland',
    'pt1': 'Portugal',
    'rs1': 'Serbia',
    'ru1': 'Russia',
    'ru2': 'Russia',
    'ru3': 'Russia',
    'se1': 'Sweden',
    'tr1': 'Turkey',
    'tr2': 'Turkey',
    'ua1': 'Ukraine',
    'ua2': 'Ukraine',
    'ua3': 'Ukraine',
    'uk1': 'United Kingdom',
    'us1': 'United States',
    'us2': 'United States',
    'us3': 'United States'
}

def check_host(url):
    if not url:
        print("Made by SpeedX\nUsage: python check.py <url>")
        return

    try:
        response = requests.get(
            f'https://check-host.net/check-http?host={url}&max_nodes=43',
            headers={'Accept': 'application/json'}
        )
        response.raise_for_status()
        data = response.json()
        request_id = data.get('request_id')
        report_link = data.get('permanent_link')
        print(f"Check initiated. Request ID: {request_id}")
        print(f"Permanent report link: {report_link}\n")

        time.sleep(20)

        result_response = requests.get(
            f'https://check-host.net/check-result/{request_id}',
            headers={'Accept': 'application/json'}
        )
        result_response.raise_for_status()
        result_data = result_response.json()

        console = Console()
        table = Table(title="Check Result", show_header=True, header_style="bold blue")
        table.add_column("No", style="dim", width=6)
        table.add_column("Region", style="bold green")
        table.add_column("Status", style="bold yellow")
        table.add_column("IP Address", style="dim")
        table.add_column("Response Time (ms)", style="dim")

        row_number = 1
        for node, data in result_data.items():
            if isinstance(data, list) and len(data) > 0:
                for result in data:
                    if result and len(result) > 3:
                        region = node_to_region.get(node.split('.')[0])
                        if region:
                            status = str(result[3])  
                            response_time = f"{result[1] * 1000:.2f}"
                            ip_address = str(result[4]) 
                            table.add_row(str(row_number), region, status, ip_address, response_time)
                            row_number += 1
                    else:
                        pass
            else:
                pass

        if table.row_count > 0:
            console.print(table)
        else:
            print("No valid results found.")
    except requests.RequestException as e:
        print("Failed to start HTTP check:", e)

check_host(sys.argv[1])

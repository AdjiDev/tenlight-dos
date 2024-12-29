import requests
from bs4 import BeautifulSoup
import random
import time
from tabulate import tabulate

class BingSearch:
    def __init__(self, query, max_pages=5):
        self.query = query
        self.halaman = max_pages
        self.base_url = "https://www.bing.com/search"
        self.headers = self.Maklo()
    
    def Maklo(self):
        uanya = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edge/95.0.1020.44",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
        ]
        return {'User-Agent': random.choice(uanya)}

    def search(self):
        r = []
        for page in range(1, self.halaman + 1):
            url = self.CariUrl(page)
            x = self.make_request(url)
            
            if x:
                pg = self.PalaBapakKau(x.text)
                r.extend(pg)
                
                time.sleep(random.uniform(2, 5))
            else:
                print(f"{page}.")
                break

        return r

    def CariUrl(self, page_number):
        start = (page_number - 1) * 10
        return f"{self.base_url}?q={self.query}&first={start+1}"

    def make_request(self, url):
        try:
            d = requests.get(url, headers=self.headers)
            if d.status_code == 200:
                return d
            else:
                print(f"Status code {d.status_code}")
                return None
        except Exception as e:
            return None

    def PalaBapakKau(self, html):
        adji = BeautifulSoup(html, 'html.parser')
        
        sr = []
        for item in adji.find_all('li', class_='b_algo'):
            tltag = item.find('h2')
            lktag = item.find('a')
            
            if tltag and lktag:
                title = tltag.get_text()
                link = lktag.get('href')
                sr.append({'title': title, 'url': link})
        
        return sr

    def GetResult(self, results):
        table = []
        for idx, result in enumerate(results, start=1):
            title = result['title']
            url = result['url']
            table.append([idx, title, url])
        
        print(tabulate(table, headers=["#", "Title", "URL"], tablefmt="fancy_grid"))
        
# query = "Python programming"
# bs = BingSearch(query, max_pages=3)  
# results = bs.search()

# bs.GetResult(results)

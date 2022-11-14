import requests
from bs4 import BeautifulSoup
import json 
import csv 
import lxml
import re
class GoogleScraper:
    pages = []
    final_data = []
    base_url = "https://www.google.com/search"
    params = {
        'q': ''
        ,'uact': '100'
        ,'oq': ''
        ,'sclient': 'gws-wiz-serp'}
    headers = {
        'authority': 'www.google.com'
        ,'accept-encoding': 'gzip, deflate, br'
        ,'accept-language': 'en-US,en;q=0.9'
        ,'cache-control': 'max-age=0'
        ,'sec-ch-ua-mobile': '?0'
        ,'sec-ch-ua-model': ""
        ,'sec-ch-ua-platform': "Windows"
        ,'sec-ch-ua-platform-version': "10.0.0"
        ,'sec-ch-ua-wow64': '?0'
        ,'sec-fetch-dest': 'document'
        ,'sec-fetch-mode': 'navigate'
        ,'sec-fetch-site': 'same-origin'
        ,'sec-fetch-user': '?1'
        ,'upgrade-insecure-requests': '1'
        ,'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    def crawler(self,html):
        content = BeautifulSoup(html,features="html.parser")
        page_links = content.findAll("a",{"class":"fl"})
        for page in page_links:
            if "/search?" in page['href']:
                print(page['href'])
                self.pages.append(page['href'])
        print(f"toatl pages for keyword {len(self.pages)}")
        #for page in page_links:
            #print(page)
    def parse(self,html):
        
        content = BeautifulSoup(html,features="html.parser")
        links = content.findAll('div',{"class":"yuRUbf"})
        for i in range(len(links)-1):
            self.final_data.append([links[i].find('h3',{"class":re.compile('LC20lb MBeuO DKV0Md')}).get_text(),links[i].find("a")['href']])
            with open("data.json","w",encoding="utf-8") as f:
                json.dump(self.final_data,f,ensure_ascii=False,indent=4)
        print(f"{len(self.final_data)} links successfuly saved!")
    def fetch(self,query):
        self.params['q'] = query
        self.params['oq'] = query
        return requests.get(self.base_url,self.params,headers=self.headers)
    def store_response(self,response):
        if response.status_code == 200:
            print('Saving response to "res.html"',end='')
            with open('res.html','w',encoding="utf-8") as html_file:
                html_file.write(response.text)
            print("\nDone")
        else:
            print("Bad Request! 404 ")
    def load_response(self):
        html = ''
        with open('res.html','r',encoding="utf-8") as html_file:
            for line in html_file.read():
                html += line 
        return html 
    def pageruner(self,q):
        print(f"Currently scraping {q}")
        return requests.get(f"https://www.google.com/{q}",headers=self.headers)
    def pagesaver(self,res):
        if res.status_code == 200:
            print('Saving response to "res.html"',end='')
            with open(f'main.html','w',encoding="utf-8") as html_file:
                html_file.write(res.text)
            print("\nDone")
        else:
            print("Bad Request! 404 ")
    def loadpage(self):
        html = ''
        with open('main.html','r',encoding="utf-8") as html_file:
            for line in html_file.read():
                html += line 
        return html
    def run(self):
        response = self.fetch(str(input("write your keyword")))
        self.store_response(response)
        html = self.load_response()
        self.crawler(html)
        for onepage in self.pages:
            mama = self.pageruner(onepage)
            self.pagesaver(mama)
            newhtml = self.loadpage()
            self.parse(newhtml)
if __name__ == "__main__":
    scraper = GoogleScraper()
    scraper.run()
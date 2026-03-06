import urllib.request
import http.cookiejar
import ssl
import sys
import time
from bs4 import BeautifulSoup
import re

# Configure stdout
sys.stdout.reconfigure(encoding='utf-8')

DHLOTTERY_MAIN_URL = 'https://www.dhlottery.co.kr/'
DHLOTTERY_URL = 'https://www.dhlottery.co.kr/lt645/result'

DHLOTTERY_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.dhlottery.co.kr/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def test_fetch():
    print("Initializing CookieJar and Opener...")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie_jar),
        urllib.request.HTTPSHandler(context=ctx)
    )
    
    # 1. Visit Main Page to get cookies
    print(f"Visiting Main Page: {DHLOTTERY_MAIN_URL}")
    req_main = urllib.request.Request(DHLOTTERY_MAIN_URL, headers=DHLOTTERY_HEADERS)
    try:
        with opener.open(req_main, timeout=20) as r:
            _ = r.read()
            print("Main page visited. Cookies:")
            for c in cookie_jar:
                print(f" - {c.name}: {c.value}")
    except Exception as e:
        print(f"Error visiting main page: {e}")
        return

    time.sleep(2) # Wait a bit like a human/server.py
    
    # 2. Visit Result Page
    print(f"Visiting Result Page: {DHLOTTERY_URL}")
    req_result = urllib.request.Request(DHLOTTERY_URL, headers=DHLOTTERY_HEADERS)
    try:
        with opener.open(req_result, timeout=20) as r:
            html = r.read().decode('utf-8', errors='replace')
            print(f"Result page fetch status: {r.status}")
            print(f"Content length: {len(html)}")
            
            # Save for inspection
            with open('test_output.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
            # 3. Parse
            parse_result(html)
            
    except Exception as e:
        print(f"Error visiting result page: {e}")

def parse_result(html):
    print("Parsing result...")
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check for result-txt
    rt = soup.find(class_=re.compile(r'result-txt'))
    if rt:
        print(f"Found result-txt: {rt.get_text(strip=True)}")
    else:
        print("NOT FOUND: result-txt")
        
    # Check for buttons/balls
    balls = soup.find_all(class_=re.compile(r'result-ball'))
    print(f"Found {len(balls)} balls.")
    for b in balls:
        print(f" - {b.get_text(strip=True)}")

    # Check specifically for drwNo (Draw Number) and Date
    rd = soup.find(class_='result-date')
    if rd:
        print(f"Found result-date: {rd.get_text(strip=True)}")
    else:
         print("NOT FOUND: result-date")

if __name__ == "__main__":
    test_fetch()

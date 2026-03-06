
import urllib.request
import ssl
import sys

# Configure stdout
sys.stdout.reconfigure(encoding='utf-8')

# Headers from server.py
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

URLS_TO_TEST = [
    'https://www.dhlottery.co.kr/lt645/result',
    'https://dhlottery.co.kr/gameResult.do?method=byWin'
]

def fetch_url(url):
    print(f"Testing URL: {url}")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers=DHLOTTERY_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as f:
            raw_content = f.read()
            try:
                content = raw_content.decode('utf-8')
                print("Decoded as UTF-8")
            except UnicodeDecodeError:
                content = raw_content.decode('euc-kr', errors='replace')
                print("Decoded as EUC-KR")
                
            print(f"Status: {f.status}")
            print(f"Content Length: {len(content)}")
            print(f"Title in content: {'<title>' in content}")
            
            # Check for winning numbers
            if 'ball_645' in content or 'result_ball' in content:
                print("Found ball/result markers!")
            else:
                print("No ball/result markers found.")
                
            # Check for specific winning number elements
            if 'drwtNo1' in content:
                 print("Found drwtNo1 script variable!")
            
            with open('debug_output.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print("Saved content to debug_output.html")

            return content
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    for url in URLS_TO_TEST:
        fetch_url(url)
        print("-" * 50)

import urllib.request
import urllib.parse
import json
import ssl
import sys
import http.cookiejar

# Configure stdout
sys.stdout.reconfigure(encoding='utf-8')

API_URL = 'https://www.dhlottery.co.kr/lt645/selectPstLt645Info.do'
MAIN_URL = 'https://www.dhlottery.co.kr/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Referer': MAIN_URL,
    'X-Requested-With': 'XMLHttpRequest'
}

def check_structure():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie_jar),
        urllib.request.HTTPSHandler(context=ctx)
    )
    
    print("Fetching API...")
    try:
        req = urllib.request.Request(f"{API_URL}?srchLtEpsd=all", headers=HEADERS, method='GET')
        with opener.open(req, timeout=15) as res:
            data = json.loads(res.read().decode('utf-8'))
            
            if 'data' in data and 'list' in data['data']:
                lst = data['data']['list']
                print(f"Got {len(lst)} items.")
                if lst:
                    item = lst[0]
                    print("First item keys:", item.keys())
                    print("First item sample:", json.dumps(item, ensure_ascii=False, indent=2))
            else:
                print("Unexpected JSON structure:", data.keys())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_structure()

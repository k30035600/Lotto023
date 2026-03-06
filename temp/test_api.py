import urllib.request
import urllib.parse
import json
import ssl
import sys
import http.cookiejar

# Configure stdout
sys.stdout.reconfigure(encoding='utf-8')

# Constants
API_URL = 'https://www.dhlottery.co.kr/lt645/selectPstLt645Info.do'
MAIN_URL = 'https://www.dhlottery.co.kr/'

HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/131.0.0.0 Safari/537.36'),
    'Referer': MAIN_URL,
    'Origin': 'https://www.dhlottery.co.kr',
    'Content-Type': 'application/json; charset=UTF-8',
    'Header-Key': 'Ajax', # Sometimes used
    'X-Requested-With': 'XMLHttpRequest'
}

def test_api():
    print("Initializing...")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie_jar),
        urllib.request.HTTPSHandler(context=ctx)
    )
    
    # 1. Visit Main to get cookies (important for session)
    print(f"visiting {MAIN_URL}...")
    try:
        opener.open(urllib.request.Request(MAIN_URL, headers=HEADERS)).read()
    except Exception as e:
        print(f"Main visit failed: {e}")

    # 2. Try POST with JSON
    print("Testing POST (JSON)...")
    data = {"srchLtEpsd": "all"}
    json_data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(
        API_URL, 
        data=json_data, 
        headers=HEADERS, 
        method='POST'
    )
    
    try:
        with opener.open(req, timeout=10) as res:
            print(f"POST Status: {res.status}")
            content = res.read().decode('utf-8')
            print(f"POST Response (first 500 chars): {content[:500]}")
    except Exception as e:
        print(f"POST Error: {e}")

    # 3. Try GET
    print("\nTesting GET...")
    params = urllib.parse.urlencode(data)
    get_url = f"{API_URL}?{params}"
    req_get = urllib.request.Request(get_url, headers=HEADERS, method='GET')
    
    try:
        with opener.open(req_get, timeout=10) as res:
            print(f"GET Status: {res.status}")
            content = res.read().decode('utf-8')
            print(f"GET Response (first 500 chars): {content[:500]}")
    except Exception as e:
        print(f"GET Error: {e}")

if __name__ == "__main__":
    test_api()

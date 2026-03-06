import urllib.request
import json
import ssl
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_specific_round(round_no):
    # 내부 API 사용
    url = f'https://www.dhlottery.co.kr/lt645/selectPstLt645Info.do?srchLtEpsd={round_no}'
    print(f"Testing API for round {round_no}: {url}")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Referer': 'https://www.dhlottery.co.kr/'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            data = r.read().decode('utf-8')
            try:
                j = json.loads(data)
                print(json.dumps(j, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("JSON decode failed")
                print(data[:200])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_specific_round(1000)

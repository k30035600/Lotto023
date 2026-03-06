# -*- coding: utf-8 -*-
"""
동행복권 결과 페이지 파싱으로 로또 당첨번호 조회 (독립 실행 스크립트)
사용: python get_lotto_numbers.py  → 최신 회차 조회
"""
import sys
import re
import urllib.request
import ssl

# Windows 콘솔 출력 인코딩 설정 (한글 깨짐 방지)
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except (AttributeError, OSError):
    pass


def _fetch_dhlottery_result_page():
    """동행복권 결과 페이지 HTML 가져오기."""
    url = 'https://www.dhlottery.co.kr/lt645/result'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=15, context=ctx) as f:
        return f.read().decode(f.headers.get_content_charset() or 'utf-8')


def _parse_lotto_from_html(html):
    """동행복권 결과 페이지 HTML에서 당첨번호 파싱."""
    vals = re.findall(r'["\']?(?:drwtNo[1-6]|bnusNo)["\']?\s*[:=]\s*["\']?(\d{1,2})["\']?', html, re.I)
    if not vals:
        vals = re.findall(r'<span[^>]*class="[^"]*ball[^"]*"[^>]*>(\d{1,2})</span>', html, re.I)
    if len(vals) >= 7:
        main = sorted([int(v) for v in vals[:6] if v.isdigit() and 1 <= int(v) <= 45])
        bonus = int(vals[6]) if vals[6].isdigit() and 1 <= int(vals[6]) <= 45 else None
        if len(main) == 6 and bonus and bonus not in main:
            drw = re.search(r'drwNo["\']?\s*[:=]\s*["\']?(\d+)["\']?', html, re.I)
            drw_no = int(drw.group(1)) if drw else None
            return {'drwNo': drw_no, 'main': main, 'bnusNo': bonus}
    return None


def get_lotto_numbers():
    """동행복권 결과 페이지 파싱으로 당첨번호 조회."""
    try:
        html = _fetch_dhlottery_result_page()
        parsed = _parse_lotto_from_html(html)
        if parsed:
            return {
                'returnValue': 'success',
                'drwNo': parsed.get('drwNo'),
                'drwtNo1': parsed['main'][0], 'drwtNo2': parsed['main'][1],
                'drwtNo3': parsed['main'][2], 'drwtNo4': parsed['main'][3],
                'drwtNo5': parsed['main'][4], 'drwtNo6': parsed['main'][5],
                'bnusNo': parsed['bnusNo']
            }
    except Exception as e:
        print(f"[Error] 동행복권 페이지 파싱 실패: {e}")
    return None


if __name__ == "__main__":
    lotto = get_lotto_numbers()

    if lotto:
        print(f"--- {lotto.get('drwNo', '?')}회 로또 결과 ---")
        print(f"당첨번호: {lotto['drwtNo1']}, {lotto['drwtNo2']}, {lotto['drwtNo3']}, "
              f"{lotto['drwtNo4']}, {lotto['drwtNo5']}, {lotto['drwtNo6']}")
        print(f"보너스번호: {lotto['bnusNo']}")
    else:
        print("당첨번호를 찾지 못했습니다.")

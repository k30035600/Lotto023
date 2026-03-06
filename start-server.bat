@echo off
cd /d "%~dp0"

echo [INFO] 패키지 설치 확인 중...
py -m pip install -r requirements.txt

echo [INFO] Playwright 브라우저 설치 확인 중...
py -m playwright install chromium

echo.
echo [INFO] 로또 서버를 시작합니다...
echo [INFO] 3초 후 브라우저가 자동으로 열립니다.
start /b cmd /c "timeout /t 3 >nul & start http://localhost:8000"
py server.py
pause
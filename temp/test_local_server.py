import urllib.request
import sys

# Configure stdout
sys.stdout.reconfigure(encoding='utf-8')

try:
    with urllib.request.urlopen("http://localhost:8000/api/lotto-latest") as response:
        print(f"Status: {response.status}")
        print(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")

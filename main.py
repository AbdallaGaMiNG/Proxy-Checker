import requests
from concurrent.futures import ThreadPoolExecutor
import sys

PROXY_FILE = 'proxies.txt' # Proxy File Name
WORK_FILE = 'work.txt' # OutPut File Name 
TEST_URL = 'https://example.com' # URL (Don't Change it, it works)
TIMEOUT = 8  # 8 seconds

def load_proxies(file):
    with open(file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_working_proxy(proxy):
    with open(WORK_FILE, 'a') as f:
        f.write(proxy + '\n')

def test_proxy(proxy):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    try:
        response = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if response.status_code == 200:
            save_working_proxy(proxy)
            return True
    except requests.RequestException:
        pass
    return False

def main():
    proxies = load_proxies(PROXY_FILE)
    total_proxies = len(proxies)
    working_count = 0

    def update_status(proxy):
        nonlocal working_count
        if test_proxy(proxy):
            working_count += 1
        sys.stdout.write(f'\rWorking Proxies: {working_count}/{total_proxies}')
        sys.stdout.flush()

    print(f'Total proxies to check: {total_proxies}')

    with ThreadPoolExecutor(max_workers=100) as executor:
        list(executor.map(update_status, proxies))

    sys.stdout.write(f'\nAll proxies checked. Working proxies saved to {WORK_FILE}.\n')

if __name__ == '__main__':
    main()

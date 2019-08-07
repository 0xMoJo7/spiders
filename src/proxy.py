from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


def get_proxy():
    ua = UserAgent()
    headers = {'user-agent': ua.random}
    proxies_req = requests.get('https://www.sslproxies.org/', headers=headers)
    soup = BeautifulSoup(proxies_req.content, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')
    proxies = []
    for row in proxies_table.tbody.find_all('tr'):
        if 'United States' in row.find_all('td')[3].string:
            proxies.append({
                'ip': row.find_all('td')[0].string,
                'port': row.find_all('td')[1].string,
                'country': row.find_all('td')[3].string
            })
    return proxies

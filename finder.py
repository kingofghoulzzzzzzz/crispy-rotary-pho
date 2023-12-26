import multiprocessing
import os
import shutil
import pyfiglet
import requests
import time
from core.controllers import Controller
from core.arguments import parse_args
from bs4 import BeautifulSoup
# Clear the terminal and get terminal size

columns, rows = shutil.get_terminal_size()



def get_content_from_sources():


  sources = [
    "https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/cnfree.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt"
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/master/proxies/http.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/http/global/http_checked.txt",
    "https://raw.githubusercontent.com/TuanMinPay/live-proxy/master/http.txt",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/http",
    "https://raw.githubusercontent.com/andigwandi/free-proxy/main/proxy_list.txt",
    "https://raw.githubusercontent.com/im-razvan/proxy_list/main/http.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/themiralay/Proxy-List-World/master/data.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
    "https://raw.githubusercontent.com/tahaluindo/Free-Proxies/main/proxies/http.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/Bardiafa/Proxy-Leecher/main/proxies.txt",
    "https://raw.githubusercontent.com/yoannchb-pro/https-proxies/main/proxies.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/file/https.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/file/http.txt",
    "https://raw.githubusercontent.com/TheLime1/Validity/main/proxy_check/proxy_list.txt",
    "https://raw.githubusercontent.com/MrMarble/proxy-list/main/all.txt",
    "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt"
  ]

  # Make an HTTP request to each URL and retrieve the content
  content = []
  for url in sources:
    response = requests.get(url)
    content.append(response.text)

  # Parse the content for proxy information, remove duplicates, and sort the proxies
  proxies = []
  for text in content:
    soup = BeautifulSoup(text, 'html.parser')
    proxies += soup.get_text().split('\n')
  proxies = list(set(proxies))
  proxies.sort()

  # Write the proxies to a file


if __name__ == "__main__":
    get_content_from_sources()
    multiprocessing.freeze_support()
    controller = Controller(
        arguments=parse_args()
    )
    try:
        controller.join_workers()
    except KeyboardInterrupt:
        pass


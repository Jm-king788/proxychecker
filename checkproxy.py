import threading
import queue
import requests

q = queue.Queue()
valid_proxies = []

with open("proxy.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)

def check_proxies():
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json",
                               proxies={"http": proxy,
                                        "https": proxy})
        except:
            continue
        if res.status_code == 200:
            valid_proxies.append(proxy)
            print(f"Valid proxy: {proxy}")

threads = []
for _ in range(10):
    thread = threading.Thread(target=check_proxies)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("Valid proxies:", valid_proxies)

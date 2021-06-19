"""
This tool is to help to fast nslookup storage.googleapis.com IPs
Concurrntly curl and find the top 3 IPs
Query the IP for location.
"""
import requests
import json
import socket
from concurrent import futures
import time
ping_count = 10
local_endpoint = "storage.googleapis.com"
query_endpoints = ["http://34.92.145.231"]
    # The access point of CloudFunction to nslookup on Cloud. Can be a list of url.

# Get region nslookup on CloudFunction
IP_list = set()
for endpoint in query_endpoints:
    try:
        response = requests.get(endpoint, timeout=3).text
        IP_list = IP_list | set(json.loads(json.dumps(eval(response))))
    except Exception as e:
        print("Can't access query_endpoints from", endpoint)
print(f"Got {len(IP_list)} IP from remote")
print("If you need to resolve IP locally, please remove the IP record of storage.googleapis.com in your local HOST file")
input("PRESS ENTER to resolve IP locally, and start PING")


# Get Local nslookup 
def getaddrinfo():
  local_list = set()
  ais = socket.getaddrinfo(local_endpoint,0,0,0,0)
  for result in ais:
    local_list.add(result[-1][0])
#   print(str(ip_list))
  return local_list

IP_list = IP_list | getaddrinfo()

# Curl IP add latency to list
def ping_ip(ip):
    global latency_list
    sum_latency = 0
    for i in range(ping_count):
        t0 = time.time()
        requests.get("http://"+ip, timeout=3)
        latency = int((time.time() - t0)*1000)
        print(ip, "    ", latency, "ms")
        sum_latency += latency
    avg_lantency = int(sum_latency / ping_count )
    latency_list.append((ip, avg_lantency))

global latency_list
latency_list = []
print(f"HTTP GET: IP {ping_count} times")
with futures.ThreadPoolExecutor(max_workers=15) as pool:
    for ip in IP_list:
        if ":" in ip:
            continue
        pool.submit(ping_ip, ip)

# Sort and print first 3 IPs
print("")
print("SORT: IP")
def takeSecond(elem):
    return elem[1]
latency_list.sort(key=takeSecond)
for l in latency_list[0:3]:
    print(l[0], "    ", l[1], "ms")
    url = f"http://ip-api.com/json/{l[0]}?fields=country,city,isp"
    try:
        response = json.loads(requests.get(url).text)
        print(response["country"], response["city"], response["isp"])
        print("")
    except Exception as e:
        print("Can't get location from", url, "ERR:", e)
print("\033[0;34;1mNOW YOU CAN PICK AN IP AND ADD TO YOUR LOCAL HOSTS FILE. FOR EXAMPLE: ")
print("")
print("sudo vi /etc/hosts")
print(latency_list[0][0], "storage.googleapis.com")
print("\033[0m")
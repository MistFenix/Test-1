import urllib
from urllib import request
import time
import ipaddress
import threading
from waiting import wait
from alive_progress import alive_bar

def url_check(ip, out):
    #print("testing")
    try:
        #print("https://" + str(ip) + "/")
        urllib.request.urlopen("https://" + str(ip) + "/", timeout=2).getcode()
    except urllib.error.URLError as e:
        if "connection" in str(e.reason):
            print("Host does not work")
        elif "handshake" in str(e.reason):
            print("Working host found!")
            out.write("https://" + str(ip) + "/" + '\n')
        global counts
        counts-=1
        
def free_threads():
    global b
    global counts
    if counts <= b:
        return True
    return False

print("Do you want to update Cloudflare ip ranges list?(y/n)")
a = str(input())
if a == "y":
    a = urllib.request.urlopen(urllib.request.Request('https://www.cloudflare.com/ips-v4', data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})).read()
    a = a.decode('utf-8')
    with open('cflare_ranges.txt', 'w') as out:
        out.write(a + '\n')
        out.close()

ips = []
with open('cflare_ranges.txt', 'r') as read:
    lines = read.readlines()
    read.close()
count = 0
for line in lines:
    ips.append([str(ip) for ip in ipaddress.IPv4Network(line[:len(line) - 1])])
    count+=1

print("How much threads do you want?")
print("Recommended: 99")
b = int(input())
counts = 0

with alive_bar(sum(len(l) for l in ips)) as bar:
    with open('cflare_output.txt', 'a') as out:
        for x in range(count):
            for y in range(len(ips[x])):
                if counts<=b:
                    threading.Thread(target=url_check, args=((str(ips[x][y])), out,)).start()
                    counts+=1
                    bar()
                else:
                    wait(lambda: free_threads(), timeout_seconds=120, waiting_for="free threads")
print("END")
out.close()

#for a in ips:

    

import urllib
from urllib import request
import time
import ipaddress
import threading
import json
from waiting import wait
from alive_progress import alive_bar
from bs4 import BeautifulSoup

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
            out.write(str(ip) + '\n')
        global counts
        counts-=1

def translator1_check(ip, out):
    global counts
    global possible_domain_count
    global parsed_domain_count
    req = urllib.request.Request('https://reverseiplookupapi.com/show_domains_with_ip.php?ip=%s' % ip, headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    the_page = urllib.request.urlopen(req).read().decode('utf-8')
    for a in json.loads(the_page):
        possible_domain_count+=a['number_of_domains']
        for domain in a['domains']:
            parsed_domain_count+=1
            out.write(domain + '\n')
    counts-=1

def free_threads():
    global threads
    global counts
    if counts <= threads:
        return True
    return False
    
def zero_threads():
    global counts
    if counts == 0:
        return True
    return False
    
def option1():
    ips = []
    with open('cflare_ranges.txt', 'r') as read:
        lines = read.readlines()
        read.close()
    count = 0
    for line in lines:
        ips.append([str(ip) for ip in ipaddress.IPv4Network(line[:len(line) - 1])])
        count+=1
    print("How much threads do you want?")
    print("Recommended: 150")
    global threads
    global counts
    threads = int(input())
    counts = 0

    with alive_bar(sum(len(l) for l in ips)) as bar:
        with open('cflare_output.txt', 'a+') as out:
            for x in range(count):
                for y in range(len(ips[x])):
                    if counts<=threads:
                        threading.Thread(target=url_check, args=((str(ips[x][y])), out,)).start()
                        counts+=1
                        bar()
                    else:
                        wait(lambda: free_threads(), timeout_seconds=120, waiting_for="free threads")
                        threading.Thread(target=url_check, args=((str(ips[x][y])), out,)).start()
                        counts+=1
                        bar()
            wait(lambda: zero_threads(), timeout_seconds=120, waiting_for="zero threads")
            print('Work Finished!')
            out.close()

def option2():
    a = str(input("Enter filename with ip_list: "))
    ips = []
    with open(a, 'r') as read:
        lines = read.readlines()
        read.close()
    for line in lines:
        ips.append(line.rstrip())
    #values = {'ip':'188.114.96.13'}
    #data = urllib.parse.urlencode(values).encode('utf-8')
    option = ''
    print('1. [FREE]ReverseIpLookup*')
    print('    *Max 10 domains per ip')
    print('2. [WIP][FREE]viewdns.info*')
    print('    *Needs proxy')
    print('3. [WIP][PAID]2ip.ru*')
    print('    *Needs captcha key + mb proxy')
    print('    *[WIP] = WorkInProgress')
    try:
        option = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')
    if option == 1:
        global threads
        global counts
        global possible_domain_count
        global parsed_domain_count
        possible_domain_count = 0
        parsed_domain_count = 0
        threads = 10
        counts = 0
        with open('ip_translator.txt', 'a+') as out:
            with alive_bar(len(ips)) as bar:
                for ip in ips:
                    if counts<=threads:
                        threading.Thread(target=translator1_check, args=((str(ip)), out,)).start()
                        counts+=1
                        bar()
                    else:
                        wait(lambda: free_threads(), timeout_seconds=120, waiting_for="free threads")
                        threading.Thread(target=translator1_check, args=((str(ip)), out,)).start()
                        counts+=1
                        bar()
            wait(lambda: zero_threads(), timeout_seconds=120, waiting_for="zero threads")
            print('Possible domain count: ' + str(possible_domain_count))
            print('Parsed domain count: ' + str(parsed_domain_count))
            out.write('Possible domain count: ' + str(possible_domain_count) + '\n')
            out.write('Parsed domain count: ' + str(parsed_domain_count) + '\n')
            out.close()
    elif option == 2:
        print('Not working for now')
        exit()
        for ip in ips:
            req = urllib.request.Request('https://viewdns.info/reverseip/?host=%s&t=1' % ip, headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            the_page = urllib.request.urlopen(req).read().decode('utf-8')
            soup = BeautifulSoup(the_page, "html.parser")
            try:
                table = (soup.find("table", {"border" : "1"})).find_all("td")
                count = 0
                with open('ip_translator.txt', 'a+') as out:
                    for link in table:
                        count+=1
                        if count % 2 == 0:
                            continue
                        elif link.get_text(strip=True) == 'Domain':
                            continue
                        else:
                            print(link.get_text)
                            out.write(link.get_text + '\n')
            except:
                continue
    elif option == 3:
        print('Not working for now')
    else:
        print('Invalid option. Please enter a number between 1 and 3.')
    #table = (soup.find("div", {"id" : "result-anchor"})).find_all("a", href=True)
    #for link in table:
    #    print(link.get('href').replace('http', 'https'))

def option3():
    a = urllib.request.urlopen(urllib.request.Request('https://www.cloudflare.com/ips-v4', data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})).read()
    a = a.decode('utf-8')
    with open('cflare_ranges.txt', 'w') as out:
        out.write(a + '\n')
        out.close()

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

menu_options = {
    1: 'CloudFlare port 443 scan',
    2: '[WIP]IP to Domain Translator(After 10 checks ip ban)',
    3: 'Update CloudFlare ranges',
    4: 'Exit',
}
        
if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            print('Goodbye!')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')



    

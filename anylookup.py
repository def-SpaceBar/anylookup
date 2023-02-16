import platform
import dns.resolver
import time
import os
import requests
import subprocess
import socket
from bs4 import BeautifulSoup

# Works properly #
def check_cmd_output(command, string_to_find):
    output = subprocess.check_output(command, shell=True, text=True)
    if string_to_find in output:
        return True
    else:
        return False

def get_OS():
    getOS = platform.system()
    return getOS

def get_current_location():
    return os.getcwd()

############
def check_directory(command, location):
    if check_cmd_output(r'{}{}'.format(command, location), 'anylookup_results'):
        return True
    else:
        return False

if check_directory('dir ', get_current_location()):
    pass
else:
    os.mkdir('anylookup_results')
############


############
def check_wordlist(command, location):
    if check_cmd_output(r'{}{}'.format(command, location), 'subdomains.txt'):
        return True
    else:
        return False

if check_wordlist('dir ', get_current_location()):
    pass
else:
    subdomains = r'{}/subdomains.txt'.format(get_current_location())
    with open('subdomains.txt','w') as subs:
        subs.close()
############


def check_subdomains(target_domain, location):
    with open(r'{}/subdomains.txt'.format(location), 'r') as subdomains:
        for subdomain in subdomains.readlines():
            try:
                sub = subdomain.split('\n')
                full_domain = f'{sub[0]}.{target_domain}'
                ip_address = socket.gethostbyname(full_domain)
                print(f"{full_domain} exists ({ip_address})")
            except socket.gaierror:
                print(f"{full_domain} does not exist")

def google_search():
    query = input('Target domain: ')
    for i in range(3):
        links = []
        page = 0 + i
        response = requests.get(f'https://www.google.com/search?q=site%3A{query}+-www+-devblogs+-docs+-developers&start={page}')
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f'\t\tpage number: {page}')
        for link in soup.find_all('a'):
            url = link.get('href')
            if url.startswith('/url?q='):
                url = url[7:]
                if '&' in url:
                    url = url.split('/')[2]
                if url in links:
                    pass
                else:
                    if 'google' in url:
                        pass
                    else:
                        links.append(url)
        for link in links:
            print(link)

def dns_query():
    global dns_query
    domain = input('Target domain: ')
    dns_types = [
        'NONE',
        'A',
        'NS',
        'MD',
        'MF',
        'CNAME',
        'SOA',
        'MB',
        'MG',
        'MR',
        'NULL',
        'WKS',
        'PTR',
        'HINFO',
        'MINFO',
        'MX',
        'TXT',
        'RP',
        'AFSDB',
        'X25',
        'ISDN',
        'RT',
        'NSAP',
        'NSAP-PTR',
        'SIG',
        'KEY',
        'PX',
        'GPOS',
        'AAAA',
        'LOC',
        'NXT',
        'SRV',
        'NAPTR',
        'KX',
        'CERT',
        'A6',
        'DNAME',
        'OPT',
        'APL',
        'DS',
        'SSHFP',
        'IPSECKEY',
        'RRSIG',
        'NSEC',
        'DNSKEY',
        'DHCID',
        'NSEC3',
        'NSEC3PARAM',
        'TLSA',
        'HIP',
        'CDS',
        'CDNSKEY',
        'CSYNC',
        'SPF',
        'UNSPEC',
        'EUI48',
        'EUI64',
        'TKEY',
        'TSIG',
        'IXFR',
        'AXFR',
        'MAILB',
        'MAILA',
        'ANY',
        'URI',
        'CAA',
        'TA',
        'DLV',
    ]
    for i in dns_types:
        entry_num = 0
        print('------------------------------')
        print(f'\t\tRecord Type: {i}')
        try:
            dns_query = dns.resolver.resolve(domain, i)
        except dns.resolver.NoAnswer:
            pass
        for x in dns_query:
            entry_num += 1
            print(f'Record Number: {entry_num}')
            print(f'\t- {x}')

def AXFR(target_domain):
    ns_response = dns.resolver.resolve(target_domain, 'NS')
    ns_list = []
    for nss in ns_response:
        ns_list.append(nss)
    print(ns_list)
    for ns in ns_response:
        print("\nTrying {}".format(ns))
        resolvedip = dns.resolver.resolve(ns.target, 'A')
        for x in resolvedip:
            print("\tResolved the NS {} - {} | Trying AXFR..".format(ns, x))
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(str(x), target_domain))
                print('\t\t\t\t\t\t--success--')
                for host in zone:
                    print("Found Host: {}".format(host))
            except Exception:
                print("Couldn't AXFR the NS {}".format(ns))
                continue

# In writing stage #


def banner():
    banner = '''
                          _                    _     _    _        
     /\                  | |                  | |   | |  | |       
    /  \    _ __   _   _ | |      ___    ___  | | __| |  | | _ __  
   / /\ \  | '_ \ | | | || |     / _ \  / _ \ | |/ /| |  | || '_ \ 
  / ____ \ | | | || |_| || |____| (_) || (_) ||   < | |__| || |_) |
 /_/    \_\|_| |_| \__, ||______|\___/  \___/ |_|\_\ \____/ | .__/ 
                    __/ |                                   | |    
                   |___/                                    |_|     \
     
    DNS Enumerator
    Made by Bar Revah (SpaceBar)
    '''
    print(banner)
banner()
time.sleep(1)
print(f'\nPlease select the wanted module:'
    f'\n1.Search Engine Enumeration'
    f'\n\t- Google'
    f'\n2.Wordlist Enumeration'
    f'\n3.DNS Record Enumeration'
    f'\n4.AXFR'
    f'\n0.exit')

choice = input('Module Number: ')
while choice != 0:
    if choice == '1':
        google_search()
        break
    if choice == '2':                 # DONE #
        brut_target = input('Target Domain: ')
        check_subdomains(brut_target, get_current_location())
        break
    if choice == '3':                 # DONE #
        dns_query()
        break
    if choice == '4':
        axfr_target_domain = input('Target Domain: ')
        AXFR(axfr_target_domain)
        break

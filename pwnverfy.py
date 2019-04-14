#!/usr/bin/env python3

import argparse
import json
import sys
import requests
from os import path
import subprocess
import inspect
from time import sleep
from termcolor import colored
from colorama import init
from termcolor import colored
from colorama import Fore, Back, Style


#################################################################
# Creating output text files for manipulating data
#################################################################

summarytbl = '/opt/pwnverfy/misc/summary.txt'
breachtbl = '/opt/pwnverfy/misc/breachtable.txt'

################################################################
# Checking if the argument has been provided
################################################################

if len(sys.argv) <= 1:
    print(colored('    [!] Missing the input file containing email addresses','yellow'))
    #print(colored('=====================================================','red'))
    print(colored('    [*] Usage: python3 pwnvrfy.py','green'),colored('emails.txt','red'))
    #print(colored('=====================================================','red'))
    exit()

################################################################
# Assigning Column Names within the Summary Table text file
################################################################

print ('\n')
print (colored('------------------------------------------------------------','blue'))
print (colored('[*] Checking Email Addresses Against HaveIBeenPwned Database ','blue'))
print (colored('------------------------------------------------------------','blue'))

c=open(summarytbl,'w')
c.write('Email Address' + '|' + 'Breach (See Table below for more details)' + '\n')

d=open(breachtbl,'w')

with open(sys.argv[1]) as f:
	for line in f.readlines():
		print ('\n')
		email = line.rstrip()
		c.write (email + '|')
		headers = {'User-Agent':'MyUserAgent'} # This can be modified to whatever string you want to send within User Agent
		req = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/'+email,headers=headers)
		try:
			data = json.loads(req.text)
		except:
			print (colored('[-] No Breach Discovered For:  ','yellow'), colored(email,'white'))
			c.write(email + '|' + 'No breach' + '|' + '\n')
			sleep(3) # sleep between checking different accounts
			continue
		print (colored("[+] Breach(es) Discovered For: ",'red'), colored(email,'white'))
		for i in data:
			chg = i['Title']
			chg2 = str(chg)
			c.write(chg2 + ',')
		c.write('|' + '\n')
		print (colored('              Associated with: ','magenta'),colored('|'), end = " ")
		for i in data:
			chg3 = str(i['Title'])
			chg4 = str(i['BreachDate'])
			print (chg3, end=' | ')
			d.write(chg3 + '|' + chg4 + '|')
			for x in i['DataClasses']:
				chg5 = str(x)
				d.write(chg5 + ',')
			d.write('|' + '\n')


########################################
# Once all the emails have been checked
# close both the files
########################################

c.close()
d.close()

###################################################################
# Cleaning the data for easier table creation
###################################################################

outfilename1 = '/opt/pwnverfy/reports/breaches_sorted.txt'
outfilename2 = '/opt/pwnverfy/reports/emails_sorted.txt'

##########################################################
# Sorting through the breach table and removing duplicates
# This step also sorts the breaches by alphabets ascending
# order.
##########################################################

lines_seen1 = set() # holds lines already seen
outfile1 = open(outfilename1, "w")
for line in open(breachtbl, "r"):
    if line not in lines_seen1: # not a duplicate
        outfile1.write(line)
        lines_seen1.add(line)
outfile1.close()

###########################################################
# The resulting dat has some extra characters. The steps
# below opens the file, reads the data, removes unnecessary
# stuff and cleans it with the delimited |
###########################################################

with open (outfilename1,'r') as myfile:
	data = myfile.read()
data2 = data.replace(',|','|')
myfile.close()

with open (outfilename1,'w') as myfile:
        myfile.write(data2)
myfile.close()

###########################################################
# The resulting dat has some extra characters. The steps  
# below opens the file, reads the data, removes unnecessary
# stuff and cleans it with the delimited | 
###########################################################

with open (summarytbl,'r') as myfile:
	data3 = myfile.read()
data4 = data3.replace(',|','|')
myfile.close()


with open (outfilename2,'w') as myfile:
	myfile.write(data4)
myfile.close()

print('\n')
print(colored('-------------------------------------------------------------','cyan'))
print(colored('[*] Script Execution Completed! See Results Folder for Output','cyan'))
print(colored('-------------------------------------------------------------','cyan'))
print('\n')

#!/usr/bin/env python3

import sys
import argparse
import requests
from colorama import Fore, Back, Style
import warnings
import os
import concurrent
import json
import time
import pkg_resources
from zipfile import ZipFile
import io
import click
from bs4 import BeautifulSoup
import validators
warnings.filterwarnings("ignore")


#check that the proper version of Wappalyzer is installed
try:
    pkg_resources.require("python-Wappalyzer>=0.4.2")
except pkg_resources.VersionConflict as e:
	#the pip version is out of date
    print(f"{Style.BRIGHT+Fore.RED}\nError: {e}")
    print(f"{Fore.BLUE}\nWappalyzer Version is unsupported, likely installed by pip. Upgrade it with the following commands: {Style.RESET_ALL}")
    print("""
pip uninstall python-Wappalyzer -y || sudo pip uninstall python-Wappalyzer -y
git clone https://github.com/brandonscholet/python-Wappalyzer /tmp/python-Wappalyzer
cd /tmp/python-Wappalyzer/
sudo python3 setup.py install
	""")
    sys.exit()

#sorry, can't set it using setup.py becuase the pip is too far behind
except Exception as e:
    print(f"{Style.BRIGHT+Fore.RED}\nError: {e}")
    print(f"{Fore.BLUE}\nInstall it with the following commands:{Style.RESET_ALL}")
    print("""
git clone https://github.com/brandonscholet/python-Wappalyzer /tmp/python-Wappalyzer
cd /tmp/python-Wappalyzer
sudo python3 setup.py install
	""")
    sys.exit()
    
#finally import
from Wappalyzer import Wappalyzer, WebPage    

def follow_meta_refresh(url):
	res = requests.get(url,verify=False)
	html_page = res.content
	soup = BeautifulSoup(html_page, 'html.parser')
	#finds all meta refresh tags
	meta_tags = soup.find_all('meta',attrs={"http-equiv":"refresh"})
	#ignore refreshes in noscript
	blacklist = ['noscript']
	for meta in meta_tags:
		if meta.parent.name not in blacklist:
			#grab wait time and url
			wait,text=meta["content"].split(";")
			#if meta refresh is less than 60 seconds
			if text.strip().lower().startswith("url=") and int(wait) < 60:
				#grab url
				redirect_url=text.strip()[4:]
				#adds local dir or overwrites with new url
				new_url = requests.compat.urljoin(url,redirect_url)
				return follow_meta_refresh(new_url)
	return url		
	
def find_valid_url(address):
	try:
		#tries to see if url is valid and allows for redirect
		temp_url=requests.head(address, verify=False, timeout=10, allow_redirects=True).url
		if not args.no_meta_refresh:
			#checks if the page redirects in under 60 seconds and then uses that url instead
			redirect_url = follow_meta_refresh(temp_url)
			#makes sense
			if temp_url.strip('/') is not redirect_url.strip('/'):
				temp_url=redirect_url
		
		return temp_url
	#handle all the errors nicely
	except requests.exceptions.HTTPError:
		raise ConnectionError(f"\n{Style.BRIGHT+Fore.RED}Http Error: {host} {Style.RESET_ALL}")
	except requests.exceptions.ConnectionError as e:
		raise ConnectionError(f"\n{Style.BRIGHT+Fore.RED}Error Connecting: {host} {Style.RESET_ALL}")
	except requests.exceptions.Timeout:
		raise ConnectionError(f"\n{Style.BRIGHT+Fore.RED}Timeout Error: {host} {Style.RESET_ALL}")
	except requests.exceptions.RequestException:
		raise ConnectionError(f"\n{Style.BRIGHT+Fore.RED}Some Other Error: {host} {Style.RESET_ALL}")
	else:
		raise ConnectionError(f"\n{Style.BRIGHT+Fore.RED}Some Other Error: {host} {Style.RESET_ALL}")
		
def save_deets(webpage_object):
		folder_url=webpage_object.url.replace('://','_').rstrip('/').replace('/','_')
		#make path for output		
		if not os.path.exists(args.scrape_dir):
			os.mkdir(args.scrape_dir)
		#make path for host		
		host_folder=args.scrape_dir+'/'+folder_url
		if not os.path.exists(host_folder):
			os.mkdir(host_folder)
		#save headers to file
		with open(host_folder+"/headers", 'w+') as header_file:
			for i,k in webpage_object.headers.items():
				header_file.write(i+' : '+k+"\n")
		#save metadata to file
		with open(host_folder+"/metadata", 'w+') as metadata_file:
			for i,k in webpage_object.meta.items():
				metadata_file.write(i+' : '+k+"\n")
		#save scripts to file
		with open(host_folder+"/scripts", 'w+') as script_file:
			for script in webpage_object.scripts:
				script_file.write(script + '\n')						
		#save pretty html to file
		with open(host_folder+"/html", 'w+') as html_file:
			pretty_html=BeautifulSoup(webpage_object.html, "html.parser").prettify()
			html_file.write(pretty_html)

def find_techs(host):
	#get's the updated file
	package_directory = os.path.dirname(os.path.abspath(__file__))
	technologies_file = os.path.join(package_directory, "technologies.json")
	#hopefully redundant strip
	host=host.strip()

	final_url=""
	try:
		#if it is already a URL, then use it
		if validators.url(host):	
			final_url = find_valid_url(host)
		else:
			#checks HTTPS and then HTTP
			for protocol in ['https://', 'http://']:
				url_string = protocol + host
				try:
					#checks URL, and allows redirects
					final_url = find_valid_url(url_string)
					if final_url:
						break
				except:
					pass
			else:
				#if http and https do not work then error out
				return ConnectionError(f"\n{Style.BRIGHT+Fore.RED}HTTP/HTTPS invalid: {host} {Style.RESET_ALL}")
	#catch invalid name from find_valid_url
	except NameError:
		raise ConnectionError(f"\n{Style.BRIGHT+Fore.RED}Host Doesn't Exist: {host} {Style.RESET_ALL}")
	#not seeing anything else here yet.	
	except Exception as e:
		raise ConnectionError(f"\n{Style.BRIGHT+Fore.RED}Unknown Error: {host} {Style.RESET_ALL}\n{e}")
		
	#actually running the only thing this program is good for
	try:
		webpage = WebPage.new_from_url(final_url, verify=False, timeout=60)
		#if you want to saved the details off for grep or whatnot		
		if args.scrape_dir:
			save_deets(webpage)
		wappalyzer= Wappalyzer.latest(technologies_file=technologies_file)
		techs = wappalyzer.analyze_with_versions_and_categories(webpage)
	except Exception as e:
		print(f"{Style.BRIGHT+Fore.RED}\n[!] WAPPALYZER ERROR: {final_url}:\n{Style.RESET_ALL}\n{e}")
	
	#display purposes
	formatted_url = final_url.split("//")[1].rstrip("/")

	#instatiate output
	output=(f"{Style.BRIGHT + Fore.BLUE}\n[+] TECHNOLOGIES {Fore.GREEN} [{formatted_url.upper()}]{Style.RESET_ALL}")
	output_file_output=""

	for tech, tech_data in techs.items():
		#print technology
		output += f"\n{tech_data['categories'][0]} : {tech}"
		#if version number is empty change to unknown, else change it to the first response
		version = "unknown" if tech_data['versions'] == [] else tech_data['versions'][0]
		#add version to output
		if version != "unknown":
			output += f" [version: {version}]"
			
		#add technology to output file listing
		if output_file:	
			output_file_output+=f"{host},{final_url.lower()},{tech_data['categories'][0]},{tech},{version}\n"
	
	#write output to file if needed
	if output_file:
		output_file.write(output_file_output)
		output_file.flush()

	#returns output to end thread
	return(output)

def parse_args():
	parser = argparse.ArgumentParser(description='''Multithreaded Web technology finder!\n\nOptional output into CSV and can save scraped site data.\n\nNote: This program also accepts hosts from STDIN with space, comma or newline delimiters.''', formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-u', '--url', nargs="+", action='extend', help='url to find technologies')
	parser.add_argument('-f', '--file', nargs="+", action='extend', help="list of urls to find web technologies")
	parser.add_argument('-wf', '--writefile', default='', help="File to write csv output to")
	parser.add_argument('-s', '--scrape_dir', nargs='?', const='.', help="save all scraped data")
	parser.add_argument('-t', '--threads', default=10, type=int, help="How many threads yo?")
	parser.add_argument('-q', '--quiet', default=False, action='store_true', help="Don't want to see any errors?")
	parser.add_argument('--no-meta-refresh', default=False, action='store_true', help="If meta refresh redirection breaks or is not what you want")

	args = parser.parse_args()

	

	#error if no argument provided
	if not args.file and not args.url and sys.stdin.isatty():
		print(parser.error('File, URL, or STDIN required'))
	return args

	
def do_the_thing():

	global args
	args=parse_args()
	urls_to_test=[]
	
	thread_count=args.threads
	suppress_errors = args.quiet
	



		
	#grep stuff redirected from STDIN. ensures to split if they are space or comma deliminated
	if not sys.stdin.isatty():
		for line in sys.stdin:
			if "," in line:
				urls_to_test.extend(line.rstrip().split(","))
			elif " " in line:
				urls_to_test.extend(line.rstrip().split(" "))
			else:
				urls_to_test.extend([line.rstrip()])

	# Check if output file is specified
	if args.writefile:
		# Open file in append mode and move cursor to the end
		global output_file 
		output_file = open(args.writefile, 'a')
		output_file.seek(0, os.SEEK_END)

		# If current position is not 0, rewind the file for future use
		if output_file.tell():
			output_file.seek(0)
		else:
			# Write header to file
			output_file.write('URL,CATEGORY,NAME,VERSION\n')
	else:
		output_file=""
	  
	# Check if input file is specified and loops to add to urls
	if args.file:
		for file in args.file:
			# Open file in read mode
			try:
				input_file = open(file, 'r')
				# Read all lines and store them in a list, while stripping
				urls_to_test.extend([line.rstrip() for line in input_file.readlines()])
			except:
				#ask if they want to skip the file or exit
				print(Style.BRIGHT+Fore.RED,f"\n[!] File Error: file {file} does not exist.\n",Style.RESET_ALL)
				if click.confirm("Do you want to skip it? No mean exiting.", default=True):
					print(f"\nSkipping {file}!")
				else:
					print("\nBetter luck next time...")
					exit()

	#adds provided urls from args.url
	if args.url:
		urls_to_test.extend(args.url)
			
	#get a unique list of urls
	urls_to_test=set(urls_to_test)

	#ensures there is at least one
	if len(urls_to_test):
		# Use ThreadPoolExecutor to run the find_techs function concurrently
		with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
			# Create a dictionary with a future object as key and the url as value
			future_to_url = {executor.submit(find_techs, i): i for i in urls_to_test}
			# Iterate through completed futures
			for future in concurrent.futures.as_completed(future_to_url):
				future_to_url[future]
				try:		
					print(future.result())
				except Exception as exc:
					#don't print errors if they don't ask
					if not suppress_errors:
						print(exc)
	else:
		print(Style.BRIGHT+Fore.RED,f"\n[!] No URLs provided.",Style.RESET_ALL)



if __name__ == "__main__":


	do_the_thing()

	
    
	


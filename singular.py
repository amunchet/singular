#!/usr/bin/env python3
'''
System for creating Plex library from RSS feed of bittorrents
	- Includes pattern matching and episode tracking
	- This file will be run on a cron during unused times
		+ All days at 3AM
'''
import feedparser
import json
import os
import sys
import time
import urllib.request
import datetime


CONFIG = "settings.json"
LOG = "singular.log"
DOWNLOAD = "data"
DELIM = "\\" # Windows specific

cmd = '''..{}..{}aria2{}aria2c.exe --seed-time=0 '''.format(DELIM, DELIM, DELIM)


def log(item):
	'''
	Logging function
	'''
	print (item)
	with open(LOG, "a+") as f:
		f.write("[" + str(datetime.datetime.now()) + "] " + str(item) + "\r\n") 
		
def read_json():
	'''
	Parses in the JSON file 
	'''
	
	return json.load(open(CONFIG, encoding="utf8"))





def read_rss(feed_url):
	'''
	Reads in the RSS feed from the given url
	'''
	log("Reading RSS")
	a = feedparser.parse(feed_url)
	return a.entries

def is_match(title, matches):
	'''
	Checks if the title is a match for the season
	'''
	
	for match in matches:
		if match.lower().replace(" ", "") in title.lower().replace(" ", ""):
			#log ("Match found!" + title + " and " + match )
			return match
			
	
	return False

def download_torrent(url, match_name, title):
	'''
	Downloads the given torrent
	'''
	
	match = match_name.replace(" ", "_")
	
	if match not in os.listdir(DOWNLOAD):
		os.system("mkdir " + DOWNLOAD + DELIM + match)
	
	if title in os.listdir(DOWNLOAD + DELIM + match):
		log(title + " already found.  Ending")
		return 1
	
	full_cmd = "cd " + DOWNLOAD + DELIM + match + " && "	
	full_cmd += cmd + '"' + url + '"'  + ''' > ..{}..{}download_output '''.format(DELIM, DELIM)
	print(os.listdir())
	log("Full command: " + full_cmd)
	os.system(full_cmd)
	with open("download_output") as f:
		log(f.read())
	
	log ("Download complete")
	
def parseName(item):
	'''
	Regex to return the proper name from a particular format from a particular feed
	'''
	try:
		return item.split("]")[1].split("-")[0].strip()
	except Exception:
		log(str(sys.exc_info()[1]))
		return -1
	
def artwork():
	'''
	Goes through each directory in data, download the artwork
	'''
	config = read_json()
	for item in config["shows"]:
		filename = item[0].replace(" ", "_")
		if filename in os.listdir(DOWNLOAD):
			if("show.jpg" not in os.listdir(DOWNLOAD + DELIM + filename)):
				log('''Thumbnail URL for {}: {}'''.format(item, item[1]))
				opener = urllib.request.build_opener()
				opener.addheaders = [('User-agent', 'Mozilla/5.0')]
				urllib.request.install_opener(opener)
				urllib.request.urlretrieve(item[1], DOWNLOAD + DELIM + filename + DELIM + "show.jpg")
			

def main():
	'''
	Main loop
	'''
	config = read_json()
	with open(LOG, "w") as f:
		f.write("[Starting]\r\n")
		
	feed = read_rss(config['rss_feed'])
	for item in feed:
		match = is_match(item.title, [x[0] for x in config['shows']])
		if(match):
			try:
				download_torrent(item.links[0].href, match, item.title)
				
			except Exception:
				log("Download error: " + str(sys.exc_info()[1]))
	
	artwork()


if __name__ == "__main__":
	main()
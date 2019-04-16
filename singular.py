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

CONFIG = "settings.json"
PICKLE = "season.pickle"
LOG = "singular.log"
DOWNLOAD = "data"

cmd = "..\\aria2\\aria2c.exe --seed-time=0 "


def log(item):
	'''
	Logging function
	'''
	print (item)
	
def read_json():
	'''
	Parses in the JSON file 
	'''
	log("Reading JSON")
	return json.load(open(CONFIG))


def read_pickle(pickle_file):
	'''
	Reads in the pickle file to determine current episodes, etc
	'''
	log("Reading pickle")
	
def write_pickle(pickle_file):
	'''
	Writes back out to the pickle file for next run
	'''
	log("Writing pickle")



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
	log("Checking for match")
	for match in matches:
		if match.lower().replace(" ", "") in title.lower().replace(" ", ""):
			log ("Match found!" + title + " and " + match )
			return match
			
	log("Match not found")
	return False

def download_torrent(url, match):
	'''
	Downloads the given torrent
	'''
	log("Downloading torrent")
	log(cmd)
	full_cmd = "cd " + DOWNLOAD + " && mkdir " + match + " && cd " + match + " && "	
	full_cmd += cmd + '"' + url + '"'  + " > ..\\..\\download_output " + 
	full_cmd += " && cd .. && cd .."
	log("Full command: " + full_cmd)
	os.system(full_cmd)
	with open("download_output") as f:
		log(f.read())
	
	log ("Download complete")
	

def main():
	'''
	Main loop
	'''
	config = read_json()
	
	feed = read_rss(config['rss_feed'])
	for item in feed:
		match = is_match(item.title, config['shows'])
		if(match):
			try:
				download_torrent(item.links[0].href, match)
			except Exception:
				log("Download error: " + str(sys.exc_info()[1]))
	



if __name__ == "__main__":
	main()
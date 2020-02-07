#!/usr/bin/env python3
"""
System for creating Plex library from RSS feed of bittorrents
	- Includes pattern matching and episode tracking
	- This file will be run on a cron during unused times
		+ All days at 3AM
"""
import feedparser
import json
import os
import sys
import time
import urllib.request
import shutil
import datetime
import glob

PATH = ""
if "SINGULAR_PATH" in os.environ:
    PATH = os.environ["SINGULAR_PATH"]


if "win32" in sys.platform.lower():
    DELIM = "\\"  # Windows specific
    cmd = """..{}..{}aria2{}aria2c.exe --seed-time=0 """.format(
        DELIM, DELIM, DELIM)

else:
    DELIM = "/"  # Linux or Mac specific
    cmd = """aria2c --seed-time=0 """.format(DELIM, DELIM, DELIM)

CONFIG = PATH + DELIM + "settings.json"
LOG = "singular.log"

DOWNLOAD = "data"
if "SINGULAR_DOWNLOAD" in os.environ:
    DOWNLOAD = os.environ["SINGULAR_DOWNLOAD"]


def log(item):
    """
    Logging function
    """
    print(item.encode("utf-8", "ignore"))
    with open(LOG, "a+") as f:
        f.write(
            "["
            + str(datetime.datetime.now())
            + "] "
            + str(item.encode("utf-8", "ignore"))
            + "\r\n"
        )


def read_json():
    """
    Parses in the JSON file 
    """

    return json.load(open(CONFIG, encoding="utf8"))


def read_rss(feed_url):
    """
    Reads in the RSS feed from the given url
    """
    log("Reading RSS")
    return [feedparser.parse(url).entries for url in feed_url]


def is_match(title, matches):
    """
    Checks if the title is a match for the season
    """

    for match in matches:
        if match.lower().replace(" ", "") in title.lower().replace(" ", ""):
            # log ("Match found!" + title + " and " + match )
            return match

    return False


def download_torrent(url, match_name, title):
    """
    Downloads the given torrent
    """

    match = match_name.replace(" ", "_")

    if match not in os.listdir(DOWNLOAD):
        os.system("mkdir " + DOWNLOAD + DELIM + match)

    if title in os.listdir(DOWNLOAD + DELIM + match):
        log(title + " already found.  Ending")
        return 1

    if len([path for path in os.listdir(DOWNLOAD + DELIM + match) if title in path]):
        log(title + " already found upon deeper inspection.  Ending")
        return 1

    full_cmd = "cd " + DOWNLOAD + DELIM + match + " && "
    full_cmd += cmd + '"' + url + '"' + " > /download_output "
    log("Full command: " + full_cmd)
    os.system(full_cmd)
    with open("/download_output") as f:
        log(f.read())

    # Fix for if they use weird naming conventions
    # Copying the files over

    for item in glob.glob(DOWNLOAD + DELIM + match + DELIM + "*Episode*"):
        if ".torrent" not in item:
            shutil.copy(item, item.replace("Episode ", "0"))

    log("Download complete")
    return 0


def thumb(match):
    """
    Generates a thumbnail for the given file
    Used for creation of thumbnails for the blog post

    This basically only works since mkdir fails if an existing directory of thumbnails already exists
    """
    path = DOWNLOAD + DELIM + match.replace(" ", "_") + DELIM

    log("Starting thumb for " + str(path))
    for item in glob.glob(path + "/*"):

        if ".torrent" not in item and ".jpg" not in item and item[-1] != "/":
            log('Starting command for ' + str(match))
            os.system("cd " + path + " && mkdir '" + item.split(".")[0] + "' && cd '" + item.split(
                ".")[0] + "' && ffmpeg -i '" + item + "' -vf scale=720:405,fps=1/15 img%03d.jpg")
            log("Finished creating thumb")
        else:
            log("Found either a torrent or an existing file in : " + item)


def parseName(item):
    """
    Regex to return the proper name from a particular format from a particular feed
    """
    try:
        return item.split("]")[1].split("-")[0].strip()
    except Exception:
        log(str(sys.exc_info()[1]))
        return -1


def artwork():
    """
    Goes through each directory in data, download the artwork
    """
    config = read_json()
    for item in config["shows"]:
        filename = item[0].replace(" ", "_")
        if filename in os.listdir(DOWNLOAD):
            if "show.jpg" not in os.listdir(DOWNLOAD + DELIM + filename):
                log("""Thumbnail URL for {}: {}""".format(item, item[1]))
                opener = urllib.request.build_opener()
                opener.addheaders = [("User-agent", "Mozilla/5.0")]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(
                    item[1], DOWNLOAD + DELIM + filename + DELIM + "show.jpg"
                )


def main():
    """
    Main loop
    """
    config = read_json()
    with open(LOG, "w") as f:
        f.write("[Starting]\r\n")

    for feed in read_rss(config["rss_feed"]):
        for item in feed:
            match = is_match(item.title, [x[0] for x in config["shows"]])
            do_thumb = 1
            if match:
                try:
                    do_thumb = download_torrent(
                        item.links[0].href, match, item.title)
                except Exception:
                    log("Download error: " + str(sys.exc_info()[1]))
                    do_thumb = 1

            temp = [x for x in config["shows"] if x[0] == match and len(
                x) > 2 and "thumbnail" in x[2] and str(x[2]["thumbnail"]) == "1"]

            if temp != []:
                log("Generating thumbnail...")
                thumb(match)

    artwork()


if __name__ == "__main__":
    main()

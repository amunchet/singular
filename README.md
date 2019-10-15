## Description
Singular is a small project aimed to perform a nightly download from an RSS feed of torrents.  

The settings.json file is in the following format:
```
{ 
  "rss_feed" : FEED_NAME,
  "shows" : 
    [SHOW_MATCHING_TEXT, ARTWORK_URL],
    ...
}
```

This is intended to have the data directory set as your Plex library and have the singular.bat script run nightly via Windows scheduling.


## Development
- Start up docker with `docker-compose singular_frontend --build -d up`
- Start up the vue development server with `cd frontend && npm run serve`
	- You can also run this in the docker, then connect on 8080 

## Requirements
- Install all of the requirements from requirements.txt
- Install Aria2 (binary also included in this repo)
- Currently configured for Windows
- Python3
- Assumes Plex server is installed

## Future
- Going to build out a Web UI for both recording information about shows watched and episode reviews.
- Want to be able to add additional shows and remove/reorganize finished ones.



### Support content creators, large and small.  Always use legal streams and torrents.

![Singular Logo](./docs/logo.png)

## Description
Singular is a small docker project aimed to perform a nightly download from an RSS feed of torrents.  It has a frontend crafted in vue to curate the `settings.json` user file.  This project was built with blogging in mind, so options for extensive types of notes exist.  It also can create automatic thumbnails from the specified episodes and has formatting options for easy copy and paste to Google Docs (or another word processor).

### General Use
Singular is intended to have the data directory set as your Plex library and have the singular.bat script run nightly via Windows scheduling or Linux cronjob.  It assumes the use of docker and specifically docker-compose.  

The frontend of Singular is meant to help keep track of shows and your thoughts on them.  General show categories are Shows (which is what you are currently watching), Completed, and Dropped.  Completed shows are ones that you can give a grade and a final review to, and Dropped are ones you just couldn't finish.

Singular is NOT a media manager.  Singular works best in conjunction with a media server, such as Plex.

## Getting Started
1.  Make sure docker and docker compose are installed
2.  ... 

## Development
- Start up docker with `docker-compose singular_frontend --build -d up`
- Start up the vue development server with `cd frontend && npm run serve`
	- You can also run this in the docker, then connect on 8080 


## Future
- Going to build out a Web UI for both recording information about shows watched and episode reviews.
- Want to be able to add additional shows and remove/reorganize finished ones.



### Support content creators, large and small.  Always use legal streams and torrents.

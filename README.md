<p align="center">
  <img src='./docs/logo.png' />
</p>

## Description
Singular is a small docker project aimed to perform a nightly download from an RSS feed of torrents.  It has a frontend crafted in vue to curate the `settings.json` user file.  This project was built with blogging in mind, so options for extensive types of notes exist.  It also can create automatic thumbnails from the specified episodes and has formatting options for easy copy and paste to Google Docs (or another word processor).

## Screenshots
![Singular Screenshot GIF](./docs/screenshot.gif)

## Key Features
- Download of torrents from RSS source
- Categorize and match by keyword
- Easy media thumbnails (for use with Plex)
- Automatic thumbnails of media
- Automatic formatting of Reviewed shows for easy transfer to Google Docs


## General Use
Singular is intended to have the data directory set as your Plex library and have the singular.bat script run nightly via Windows scheduling or Linux cronjob.  It assumes the use of docker and specifically docker-compose.  

The frontend of Singular is meant to help keep track of shows and your thoughts on them.  General show categories are Shows (which is what you are currently watching), Completed, and Dropped.  Completed shows are ones that you can give a grade and a final review to, and Dropped are ones you just couldn't finish.

Singular is NOT a media manager.  Singular works best in conjunction with a media server, such as Plex.

## Getting Started
0.  PLEASE NOTE: Currently the docker-compose is setup for use with traefik.  If you wish to use singular standalone, simply uncomment the lines in docker-compose for the port to expose the port directly.
1.  Make sure docker and docker compose are installed
2.  Modify `docker-compose.yml` to fit needs
3.  Run either `start_prod.sh` if on Linux.  For Windows or Mac, run the appropriate dockers from docker-compose (i.e. `docker-compose up --build -d singular_backend`).  If you are not using `start_prod.sh`, read the contents to build the vue project manually.
4.  Navigate to port 7500 for the frontend interface
5.  Setup Cron or some kind of timed event to run the `singular_cli`.  This will automatically download on a schedule

### Development
- Start up docker with `docker-compose singular_frontend --build -d up`
- Start up the vue development server with `cd frontend && npm run serve`
	- You can also run this in the docker, then connect on 8080 
- Fix the bug, add the feature, and issue a PR!


# Support content creators, large and small.  Always use legal streams and torrents.

#!/bin/sh

# Command to test if the old singular docker is running

COUNT=`docker ps | grep singular | wc | awk ' { print $1 } '`

if [ "$COUNT" -eq "1" ]; then
	echo "Only Singular backend running.  Going ahead..."
	/usr/local/bin/docker-compose up singular_cli
fi

if [ "$COUNT" -eq "2" ]; then
	echo "Singular client still running.  Exiting."
fi

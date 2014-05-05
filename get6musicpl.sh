#!/bin/bash
curl -s http://www.bbc.co.uk/6music/playlist|egrep "playlist-item-artist|playlist-item-title"|cut -d\> -f2|cut -d\< -f1|awk 'ORS=NR%2?" - ":"\n"'

import sys
from gmusicapi import Mobileclient
import requests
import re
import codecs

api = Mobileclient()
username = sys.argv[1]
password = sys.argv[2]

def google_login():
  logged_in = api.login(username, password)
  return logged_in

def get_playlist():
  r = requests.get('http://www.bbc.co.uk/6music/playlist')
  artists = re.findall(r'<div[^>]*class\s*=\s*([\"\'])pll-playlist-item-artist\1[^>]*>(.*?)</div>', r.text)
  songs = re.findall(r'<div[^>]*class\s*=\s*([\"\'])pll-playlist-item-title\1[^>]*>(.*?)</div>', r.text)
  artists = [tup[1] for tup in artists]
  artists = [string.encode('utf8', 'replace') for string in artists]
  songs = [tup[1] for tup in songs]
  songs = [string.encode('utf8', 'replace') for string in songs]
  count = 0
  titles = range(len(artists))
  while count != len(artists):
    titles[count] = artists[count] + " - " + songs[count]
    count = count + 1
  return titles

def get_store_id(search_string):
  details = api.search_all_access(search_string, max_results=1)
  song_hits = details['song_hits']
  tracks = song_hits[0]
  storeId = tracks['track']['storeId']
  return storeId

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

google_login()
playlist = api.create_playlist('BBC 6 Music Playlist')

for track in get_playlist():
  try:
    track = strip_non_ascii(track)
    store_id = get_store_id(track)
    api.add_songs_to_playlist(playlist, store_id)
    print "Track added: " + track
  except Exception, exc:
    print "Cannot find " + track

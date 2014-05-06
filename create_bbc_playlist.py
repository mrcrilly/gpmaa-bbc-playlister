import sys
from gmusicapi import Mobileclient
import requests
import re
import codecs

api = Mobileclient()
username = sys.argv[1]
password = sys.argv[2]
bbc_station = sys.argv[3]

def verify_args():
  if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
    print "Username invalid. Please enter your google username (probably your gmail address)"
    return "fail"
  passed = "fail"
  for station in ["1xtra", "radio1", "radio2", "6music", "asiannetwork", "radioscotland"]:
    if bbc_station == station:
      passed = "pass"
  if passed == "fail":
    print "This is not a BBC Station (Or at least, not one which provides a playlist)"
    return "fail"
  return "pass"

def google_login():
  logged_in = api.login(username, password)
  if logged_in == 0:
    print "Login failed. Are you a Google Play Music All Access subscriber?"
  return logged_in

def get_playlist():
  bbc_playlist = 'http://www.bbc.co.uk/' + bbc_station + '/playlist'
  r = requests.get(bbc_playlist)
  artists = re.findall(r'<div[^>]*class\s*=\s*([\"\'])pll-playlist-item-artist\1[^>]*>(.*?)</div>', r.text)
  songs = re.findall(r'<div[^>]*class\s*=\s*([\"\'])pll-playlist-item-title\1[^>]*>(.*?)</div>', r.text)
  playlist_name = re.findall(r'<title>(.*?)</title>', r.text)
  artists = [tup[1] for tup in artists]
  artists = [string.encode('utf8', 'replace') for string in artists]
  songs = [tup[1] for tup in songs]
  songs = [string.encode('utf8', 'replace') for string in songs]
  playlist_name = playlist_name[0].encode('utf8', 'replace')
  count = 0
  titles = range(len(artists))
  while count != len(artists):
    titles[count] = artists[count] + " - " + songs[count]
    count = count + 1
  return titles, playlist_name

def get_store_id(search_string):
  details = api.search_all_access(search_string, max_results=1)
  song_hits = details['song_hits']
  tracks = song_hits[0]
  storeId = tracks['track']['storeId']
  return storeId

def strip_non_ascii(string):
  stripped = (c for c in string if 0 < ord(c) < 127)
  return ''.join(stripped)

def get_playlist_id(playlist):
  playlist = re.sub("- ", "", playlist)
  extant_playlists = api.get_all_playlists(incremental=False, include_deleted=False)
  extant_playlist = "False"
  for playlists in extant_playlists:
    if playlists['name'] == playlist:
      extant_playlist = "True"
      playlist_id = playlists['id']
  if extant_playlist == "True":
    all_playlist_contents = api.get_all_user_playlist_contents()
    for playlist_contents in all_playlist_contents:
      if playlist_contents['id'] == playlist_id:
        for track in playlist_contents['tracks']:
          api.remove_entries_from_playlist(track['id'])
    return playlist_id
  else:
    playlist_id = api.create_playlist(playlist)
    return playlist_id

if verify_args() == "pass":
  if google_login() == 1:
    tracks_playlistname = get_playlist()
    tracks = tracks_playlistname[0]
    playlist = get_playlist_id(tracks_playlistname[1])
    for track in tracks:
      try:
        track = strip_non_ascii(track)
        store_id = get_store_id(track)
        api.add_songs_to_playlist(playlist, store_id)
        print "Track added: " + track
      except Exception, exc:
        print "Cannot find " + track
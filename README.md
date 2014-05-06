Google Play Music All Access BBC Radio Playlister
=================================================

Or GPMAA-BBCRP for short..
--------------------------

This little python script pulls playlists from the BBC website and pushes it into your GPMAA account as a playlist. It also does sensible things like delete the playlist contents before repopulating it, instead of just deleting the playlist (or adding extra tracks, or adding a second playlist) - this conserves shared playlist links.

Use
---

    python create_bbc_playlist.py <google-username> <google-password> <BBC-Radio-Station>

Currently tested with:

- BBC Radio 1xtra (1xtra)
- BBC Radio 1 (radio1)
- BBC Radio 2 (radio2)
- BBC Radio 6 Music (6music)
- BBC Radio Scotland (radioscotland)
- BBC Asian Network (asiannetwork)

Note that it can only match against tracks that exist in GPMAA - if it doesn't exist, it won't be in the playlist.

Oh I can't be bothered - can't I just use your playlist?
--------------------------------------------------------

Sure! [Check here!](http://james.belchamber.com/gpmaa-bbc-playlister.html)

# import spotipy
# import ctypes
# import os
# import urllib

# lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

# spotify = spotipy.Spotify()
# results = spotify.artist_top_tracks(lz_uri)
# SPI_SETDESKWALLPAPER = 20
# index = 0            # Python's indexing starts at zero
# for track in results['tracks'][:10]:
#     print 'track    : ' + track['name']
#     print 'audio    : ' + track['preview_url']
#     print 'cover art: ' + track['album']['images'][0]['url']
#     #retrives the albumn art from online and saves it
#     indexString = str(index)
#     urllib.urlretrieve(track['album']['images'][0]['url'], "0000000"+indexString+".jpg")
#     index += 1
# #gets the current directory
# cwd = os.getcwd()
# #adds the image to the current directory
# image_path = os.path.join(cwd, "00000002.jpg")
# #changes the desktop background to said image
# ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image_path, 3)
import sys
import spotipy
import spotipy.util as util



PORT_NUMBER = 8080
export SPOTIPY_CLIENT_ID='0aba7752b92a456dbd489873b3d80dea'
export SPOTIPY_CLIENT_SECRET='0742e0abc2864e56ad8d39871beb72d3'
export SPOTIPY_REDIRECT_URI='http://nickengmann.com'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print track['name'] + ' - ' + track['artists'][0]['name']
else:
    print "Can't get token for", username
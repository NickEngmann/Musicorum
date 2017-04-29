from bottle import route, run, request
import spotipy
from spotipy import oauth2
import ctypes
import os
import urllib
import requests
import time

PORT_NUMBER = 3000
#Spotify Credentials
SPOTIPY_CLIENT_ID='0aba7752b92a456dbd489873b3d80dea'
SPOTIPY_CLIENT_SECRET='0742e0abc2864e56ad8d39871beb72d3'
SPOTIPY_REDIRECT_URI = 'http://localhost:3000'
SCOPE = 'user-library-read user-read-currently-playing user-read-playback-state'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )
#timeout for refreshing
timeout = 4 # Four seconds
access_token = ""
refresh_token = ""
@route('/')
def index():
    #get the cached tokens if they exist
    token_info = sp_oauth.get_cached_token()
    if token_info:
        print "Found cached token!"
        access_token = token_info['access_token']
        refresh_token = token_info['refresh_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print "Found Spotify auth code in Request URL! Trying to get valid access token..."
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']
            refresh_token = token_info['refresh_token']
    if access_token:
        # changeBackground(access_token)    
        while True:
            #every four seconds attempt to change the background
            time.sleep(4)
            #schedule.every(5).seconds.do(changeBackground(access_token))
            try:
                changeBackground(access_token)
            except:
                #if exception rises that means that the access token has expired, if that is the case, then go ahead and get a new access token with the fresh token
                body_params = {'grant_type' : refresh_token}
                response=requests.post(url, data=body_params, auth = (client_id, client_secret))
                r= response.json()
                tokens = r['access_token']
                access_token = r['access_token']
                refresh_token = r['refresh_token']
        return "<html>WORKING</html>"
    else:
        return htmlForLoginButton()

def changeBackground(token):
        #get request with spotify API, get the currently playing song
        results = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers={'Authorization':'Bearer ' + token})
        r = results.json()
        image = r['item']['album']['images'][0]['url']
        urllib.urlretrieve(image, "current.jpg")
        #gets the current directory
        cwd = os.getcwd()
        #adds the image to the current directory
        SPI_SETDESKWALLPAPER = 20
        image_path = os.path.join(cwd, "current.jpg")
        #changes the desktop background to said image
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image_path, 3)
        #return r        #returns the json response
        # return "<html></html>"

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

run(host='', port=3000)
# reactor.run()
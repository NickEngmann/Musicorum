import requests


client_id='0aba7752b92a456dbd489873b3d80dea'
client_secret='0742e0abc2864e56ad8d39871beb72d3'
grant_type = 'client_credentials'
scope = 'user-library-read user-read-currently-playing user-read-playback-state'
#Request based on Client Credentials Flow from https://developer.spotify.com/web-api/authorization-guide/

#Request body parameter: grant_type Value: Required. Set it to client_credentials
body_params = {'grant_type' : grant_type}

url='https://accounts.spotify.com/api/token'

response=requests.post(url, data=body_params, auth = (client_id, client_secret)) 
r= response.json()
tokens = r['access_token']
results = requests.get('https://api.spotify.com/v1/me/tracks', headers={'Authorization':'Bearer ' + tokens })
print results
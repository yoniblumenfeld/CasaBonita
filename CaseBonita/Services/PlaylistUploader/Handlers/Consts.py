CHROMEDRIVER = "/home/yovel/PycharmProjects/chromedriver"
APPLEMUSIC_LOGIN_PAGE = 'https://music.apple.com/us/artist/login/439834157'

CLIENT_ID = 'c13f9174976545dc88adabebe21d7e56'

CLIENT_SECRET = '4ebe64f377994602b0ebf12232ab4d2b'

# For development server
LOCAL_SERVER = 'http://0.0.0.0:7000/'

# Ask for user credential.
SPOTIFY_USER_ACCESS = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&redirect_uri={LOCAL_SERVER}&scope=user-read-private%20user-read-email&response_type=token&state=123"

SCOPE = 'playlist-modify-private'
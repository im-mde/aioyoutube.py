import asyncio
import os
from aioyoutube import YouTubeAuthClient
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

# Reference: https://developers.google.com/youtube/v3/docs/channels/update

# load secrets
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
OAUTH_FILE = 'oauth2.json'

SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl'
]


"""
    Google code to authenticate a YouTube account via a browser, instructing you to copy
    the temporary secret into stdin, and returning an Oauth2 token used to make authenticated
    HTTP requests. Oauth authentication is an important concept and it's best to research
    before using a third-party library or even more so if you implement it yourself. This
    method involves inputting a json file with your OAuth secret information. Look at 
    Google's api client repositories for more information.
""" 
def authenticate_from_console(client_secret_file: str, scopes: list, **kwargs):

    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes, **kwargs)
    credentials = flow.run_console()
    return credentials.token


# updates information on a YouTubeChannel and prints out response
async def update_channel(data: dict, part: list):

    token = authenticate_from_console(OAUTH_FILE, SCOPES)
    #client = YouTubeAuthClient.from_token_connect(key=YOUTUBE_API_KEY, 
    #    token=token, http_exceptions=False)

    #client = YouTubeAuthClient(key=YOUTUBE_API_KEY, token=token)

    # utilizes context manager to automatically close after going out of scope due 
    # to being a one-off
    async with YouTubeAuthClient(key=YOUTUBE_API_KEY, token=token) as youtube:
        result = await youtube.update(resource='channel', part=part, data=data)
        print(result.status, result.data, result.headers)

    #result = await client.update(resource='channel', part=part, data=data)
    #await client.close()

if __name__ == '__main__':    

    # The provided data will update the channel description of a channel
    # with the given channel id.
    data = {
        'id': 'Channel Id Here',
        'brandingSettings': {
            'channel': {
                'description': 'This is a test description for my YouTube Channel!'
            }
        }
    }

    part = ['brandingSettings']

    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_channel(data, part))
    loop.close()
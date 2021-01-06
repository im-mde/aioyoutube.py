from asyncio import AbstractEventLoop
from aiohttp import ClientSession
from aioyoutube.http import YouTubeAPISession
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import asyncio
import json

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
VALID_RATINGS = {'like', 'dislike', 'none'}

def parse_kind(kind):
    if 'youtube#' in kind:
        if kind[-1] != 's' and kind != 'search': 
            kind += 's'
        return kind.split('#')[1]
    elif type(kind) == str:
        if kind[-1] != 's' and kind != 'search':
            kind += 's'
        return kind
    else:
        raise TypeError

def build_endpoint(query_type: str, key: str, part: list = [], **kwargs):
    endpoint = '{}?'.format(query_type)
    if len(part) > 0:
        part = ','.join(part)
        endpoint = '{}?part={}'.format(query_type, part)
    
    for key_, value in kwargs.items():
        endpoint += '&{}={}'.format(key_, str(value))
    
    return endpoint + '&key={}'.format(key)

class YouTubeAPIClient:

    """
        Represents a client object used to interact with the YouTube Data API.

        Parent(s):
            None
        
        Attribute(s):
            key typ(str): YouTube API key
            loop typ(asyncio.AbstractEventLoop): event loop for async operations
            session typ(aiohttp.ClientSession): async http session

        Method(s):
            search ret():
            create ret():
            delete ret():
            update ret():
            download ret():
            rate ret():
            get_rating ret():
            report_abuse ret():
            close_session ret(None): closes the http session
    """

    QUOTA_LIMIT = 10000

    def __init__(self, key: str):
        self.key = key
        self.loop = None
        self.session = None
        self.credentials = None
        self.service = None

    async def connect(self, session: YouTubeAPISession = None, loop: AbstractEventLoop = None):
        self.session = session or YouTubeAPISession(loop=loop)
        self.loop = loop or asyncio.get_event_loop()

    async def authenticate_from_console(self, client_secret_file: str, scopes: list, **kwargs):
        self.flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes, **kwargs)
        self.credentials = self.flow.run_console()
        self.service = build(API_SERVICE_NAME, API_VERSION, credentials=self.credentials)

    @classmethod
    async def from_connect(cls, key: str, session: YouTubeAPISession = None, loop: AbstractEventLoop = None):
        class_ = cls(key)
        class_.loop = loop or asyncio.get_event_loop()
        class_.session = session or YouTubeAPISession(loop=loop)
        class_.credentials = None
        return class_

    async def rate(self, video_id: str, rating: str):
        if rating not in VALID_RATINGS:
            raise ValueError('rating argument must be one of %r' % VALID_RATINGS)

        endpoint = build_endpoint('videos/rate', self.key, part=[], id=id, rating=rating)

        return await self.session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self.credentials.token)})

    async def search(self, search_term: str, json: bool = True, **kwargs):
        return await self.itemize(kind='search', part=['snippet'], 
            json=json, q=search_term, **kwargs
        )        

    async def insert(self, body, part = None, **kwargs):
        NotImplemented

    async def delete(self, body, part = None, **kwargs):
        NotImplemented

    async def update(self, body, part = None, **kwargs):
        NotImplemented

    # replaces "list" from api documentation due to it being a python keyword
    async def itemize(self, kind, part: list, json: bool = True, **kwargs):
        if self.session == None:
            raise Exception
        else:
            query_type = parse_kind(kind)
            endpoint = build_endpoint(query_type, self.key, part, **kwargs)
            result = await self.session.get(endpoint=endpoint)
            
            if not json:
                pass
            else:
                return await result.json()

    async def download(self, part = None, **kwargs):
        NotImplemented
    
    async def close_session(self):
        await self.session.close()
from asyncio import AbstractEventLoop
from aiohttp import ClientSession
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import asyncio
import json

from .http import YouTubeAPISession
from .parse import build_data, build_endpoint, parse_kind
from .valid import *

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

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
        if rating not in RATINGS:
            raise ValueError('rating argument must be one of %r' % RATINGS)

        endpoint = build_endpoint('videos/rate', self.key, part=[], id=id, rating=rating)

        return await self.session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self.credentials.token)})

    async def set_(self):
        NotImplemented

    async def search(self, search_term: str, **kwargs):
        return await self.list_(kind='search', part=['snippet'], 
            q=search_term, **kwargs
        )        

    async def insert(self, kind: str, part: list = [], **kwargs):
        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self.key, part=part)
        data = build_data(**kwargs)
        print(data)

        result = await self.session.put(endpoint=endpoint, data=data,
            headers={'Authorization': 'Bearer {}'.format(self.credentials.token),
                'Content-Type': 'application/octet-stream'})
        return await result.json()

    async def delete(self, kind: str, id: str, **kwargs):
        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self.key, id=id)

        result = await self.session.delete(endpoint=endpoint, 
            headers={'Authorization': 'Bearer {}'.format(self.credentials.token)})
        return await result.json()

    async def update(self, kind, part: list = [], **kwargs):
        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self.key, part=part)
        data = build_data(**kwargs)

        result = await self.session.put(endpoint=endpoint, data=json.dumps(data), 
            headers={'Authorization': 'Bearer {}'.format(self.credentials.token),
                'Content-Type': 'application/json'})
        return await result.json()

    # replaces "list" from api documentation due to it being a python keyword
    async def list_(self, kind, part: list, **kwargs):
        if self.session == None:
            raise Exception
        else:
            query_type = parse_kind(kind)
            endpoint = build_endpoint(query_type, self.key, part, **kwargs)
            result = await self.session.get(endpoint=endpoint)
            return await result.json()

    async def download(self, kind: str, id: str, **kwargs):
        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self.key, **kwargs)

        result = await self.session.get(endpoint=endpoint, id=id, **kwargs,
            headers={'Authorization': 'Bearer {}'.format(self.credentials.token)})
        return await result.json()
    
    async def close_session(self):
        await self.session.close()
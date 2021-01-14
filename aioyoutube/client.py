from asyncio import AbstractEventLoop
from aiohttp import ClientSession
import asyncio
import json

from .http import YouTubeAPISession
from .parse import build_data, build_endpoint, parse_kind
from .valid import RATINGS

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
            update ret():    @classmethod
    async def from_connect(cls, key: str, token: str = None, session: YouTubeAPISession = None, loop: AbstractEventLoop = None):
        
        class_ = cls(key, token)
        class_.loop = loop or asyncio.get_event_loop()
        class_.session = session or YouTubeAPISession(loop=class_.loop)
        return class_
            download ret():
            rate ret():
            get_rating ret():
            report_abuse ret():
            close_session ret(None): closes the http session
    """

    QUOTA_LIMIT = 10000

    def __init__(self, key: str, token: str = None):

        self.key = key
        self._token = token or None
        self.loop = None
        self.session = None

    @classmethod
    async def from_connect(cls, key: str, token: str = None, session: YouTubeAPISession = None, loop: AbstractEventLoop = None):
        
        class_ = cls(key, token)
        class_.loop = loop or asyncio.get_event_loop()
        class_.session = session or YouTubeAPISession(loop=class_.loop)
        return class_

    async def connect(self, session: YouTubeAPISession = None, loop: AbstractEventLoop = None):
        
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or YouTubeAPISession(loop=self.loop)

    async def close(self):
        await self.session.close()

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value: str):
        self._token = value

    async def rate(self, id: str, rating: str, token: str = None):
        
        self._token = token or self._token

        if rating not in RATINGS:
            raise ValueError('rating argument must be one of %r' % list(RATINGS))

        endpoint = build_endpoint('videos/rate', self.key, part=[], id=id, rating=rating)

        return await self.session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})

    async def getRating(self, id: list, **kwargs):
        NotImplemented

    async def reportAbuse(self, videoId_: str, reasonId_: str, **kwargs):
        NotImplemented

    async def set_(self):
        NotImplemented

    async def search(self, search_term: str, **kwargs):
        return await self.list_(kind='search', part=['snippet'], 
            q=search_term, **kwargs
        )        

    async def insert(self, kind: str, part: list = [], token: str = None, **kwargs):
        
        self._token = token or self._token

        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self.key, part=part)
        data = build_data(**kwargs)
        print(data)

        result = await self.session.put(endpoint=endpoint, data=data,
            headers={'Authorization': 'Bearer {}'.format(self._token),
                'Content-Type': 'application/octet-stream'})
        return await result.json()

    async def delete(self, kind: str, id: str, token: str = None, **kwargs):

        self._token = token or self._token

        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self.key, id=id)

        result = await self.session.delete(endpoint=endpoint, 
            headers={'Authorization': 'Bearer {}'.format(self._token)})
        return await result.json()

    async def update(self, kind, part: list = [], token: str = None, **kwargs):
        
        self._token = token or self._token

        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self.key, part=part)
        data = build_data(**kwargs)

        result = await self.session.put(endpoint=endpoint, data=json.dumps(data), 
            headers={'Authorization': 'Bearer {}'.format(self._token),
                'Content-Type': 'application/json'})
        return await result.json()

    async def list_(self, kind, part: list, token: str = None, **kwargs):
        
        self._token = token or self._token

        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type, self.key, part, **kwargs)
        
        headers=None
        if self._token != None:
            headers = {'Authorization': 'Bearer {}'.format(self._token)}

        result = await self.session.get(endpoint=endpoint,
            headers=headers)
        return await result.json()

    async def download(self, kind: str, id: str, token: str = None, **kwargs):
        
        self._token = token or self._token

        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self.key, **kwargs)

        result = await self.session.get(endpoint=endpoint, id=id, **kwargs,
            headers={'Authorization': 'Bearer {}'.format(self._token)})
        return await result.json()
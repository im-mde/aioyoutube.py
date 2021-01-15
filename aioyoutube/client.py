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

    def __init__(self, key: str):

        self._key = key
        self._session = None

    @classmethod
    async def from_connect(cls, key: str, session: YouTubeAPISession = None, loop: AbstractEventLoop = None):
        
        class_ = cls(key)
        loop_ = loop or asyncio.get_event_loop()
        class_._session = session or YouTubeAPISession(loop=loop_)
        return class_

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value: str):
        self._key = value

    async def connect(self, session: YouTubeAPISession = None, loop: AbstractEventLoop = None):
        
        loop_ = loop or asyncio.get_event_loop()
        self._session = session or YouTubeAPISession(loop=loop_)

    async def close(self):
        await self._session.close()

    async def list_(self, kind, part: list, token: str = None, **kwargs):

        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type, self._key, part, **kwargs)
        
        headers=None
        if token != None:
            headers = {'Authorization': 'Bearer {}'.format(token)}

        result = await self._session.get(endpoint=endpoint, headers=headers)
        return await result.json()

class YouTubeBaseClient(YouTubeAPIClient):

    def __init__(self, key: str):
        super().__init__(key)

    async def search(self, search_term: str, **kwargs):
        return await self.list_(kind='search', part=['snippet'], 
            q=search_term, **kwargs)        

    async def list_(self, kind, part: list, **kwargs):
        return await super().list_(kind=kind, part=part, **kwargs)
    
class YouTubeAuthClient(YouTubeAPIClient):

    def __init__(self, key: str, token: str):
        self._token = token
        super().__init__(key)
    
    @classmethod
    async def from_token_connect(cls, key: str, token:str, session: YouTubeAPISession = None, loop: AbstractEventLoop = None):
        
        class_ = cls(key, token)
        loop_ = loop or asyncio.get_event_loop()
        class_._session = session or YouTubeAPISession(loop=loop_)
        return class_

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value: str):
        self._token = value

    async def insert(self, kind: str, part: list = [], **kwargs):
        
        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self._key, part=part)
        data = build_data(**kwargs)
        print(data)

        result = await self._session.put(endpoint=endpoint, data=data,
            headers={'Authorization': 'Bearer {}'.format(self._token),
                'Content-Type': 'application/octet-stream'})
        return await result.json()

    async def delete(self, kind: str, id: str, **kwargs):

        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self._key, id=id)

        result = await self._session.delete(endpoint=endpoint, 
            headers={'Authorization': 'Bearer {}'.format(self._token)})
        return await result.json()

    async def update(self, kind: str, part: list = [], **kwargs):
        
        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self._key, part=part)
        data = build_data(**kwargs)

        result = await self._session.put(endpoint=endpoint, data=json.dumps(data), 
            headers={'Authorization': 'Bearer {}'.format(self._token),
                'Content-Type': 'application/json'})
        return await result.json()
    
    async def set_(self):
        NotImplemented

    async def list_(self, kind: str, part: list, **kwargs):
        return await super().list_(kind, part, token=self._token, **kwargs)

    async def rate(self, id: str, rating: str):
        
        if rating not in RATINGS:
            raise ValueError('rating argument must be one of %r' % list(RATINGS))

        endpoint = build_endpoint('videos/rate', self._key, part=[], id=id, rating=rating)

        return await self._session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})

    async def download(self, kind: str, id: str, **kwargs):
        
        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type=query_type, key=self._key, **kwargs)

        result = await self._session.get(endpoint=endpoint, id=id, **kwargs,
            headers={'Authorization': 'Bearer {}'.format(self._token)})
        return await result.json()

    async def getRating(self, id: list, **kwargs):
        NotImplemented

    async def reportAbuse(self, videoId_: str, reasonId_: str, **kwargs):
        NotImplemented

class YouTubeCrossClient(YouTubeAuthClient, YouTubeBaseClient):

    def __init__(self, key: str, token: str):
        super().__init__(key, token)

    async def list_(self, kind: str, part: str, auth: bool = True, **kwargs):
        if auth:
            return await super().list_(kind, part, **kwargs)
        else:
            return await YouTubeBaseClient.list_(self, kind, part, **kwargs)
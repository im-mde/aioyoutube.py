from asyncio import AbstractEventLoop
from aiohttp import ClientSession
import asyncio
import json
import base64

from .http import YouTubeAPISession, YouTubeAPIResponse
from .parse import parse_resource, build_endpoint
from .valid import RATINGS

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

class YouTubeAPIClient:

    """
        Foundational client object for the YouTube Data API.

        An object of this class should not be directly initialized
        
        Parent(s):
            None
        
        Attribute(s):
            key type(str): YouTube API key 
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

    async def list_(self, resource, part: list, token: str = None, **kwargs):

        query_type = parse_resource(resource)
        endpoint = build_endpoint(query_type=query_type, key=self._key, part=part, **kwargs)
        
        headers=None
        if token != None:
            headers = {'Authorization': 'Bearer {}'.format(token)}

        result = await self._session.get(endpoint=endpoint, headers=headers)
        
        return YouTubeAPIResponse(await result.json(), result.status)

class YouTubeBaseClient(YouTubeAPIClient):
    
    """
        Client object for making YouTube API requests w/o an access token.
        
        Use this client when you are wanting to access less sensitive data 
        from the YouTube Data API.
        
        Parent(s):
            YouTubeAPIClient
        
        Attribute(s):
            key type(str): YouTube API key 
    """

    def __init__(self, key: str):
        super().__init__(key)

    async def search(self, search_term: str, **kwargs):
        return await self.list_(resource='search', part=['snippet'], 
            q=search_term, **kwargs)        

    async def list_(self, resource, part: list, **kwargs):
        return await super().list_(resource=resource, part=part, **kwargs)
    
class YouTubeAuthClient(YouTubeAPIClient):

    """
        Client object for making YouTube API requests with an access token.
        
        Use this client when you are wanting access to sensitive information
        and/or implementing actions such as liking a video.
        
        Parent(s):
            YouTubeAPIClient
        
        Attribute(s):
            key type(str): YouTube API key
            token type(str): Access token
    """

    def __init__(self, key: str, token: str):
        self._token = token
        super().__init__(key)
    
    @classmethod
    async def from_token_connect(cls, key: str, token: str, session: YouTubeAPISession = None, loop: AbstractEventLoop = None):
        
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

    async def list_(self, resource: str, part: list, **kwargs):
        return await super().list_(resource, part, token=self._token, **kwargs)

    # TODO: YET TO BE PROPERLY IMPLEMENTED
    async def insert(self, resource: str, data: dict, part: list = [], **kwargs):
        
        query_type = parse_resource(resource)
        endpoint = build_endpoint(query_type=query_type, key=self._key, part=part, **kwargs)

        result = await self._session.put(endpoint=endpoint, data=data,
            headers={'Authorization': 'Bearer {}'.format(self._token),
                'Content-Type': 'application/octet-stream'})
        return await result.json()

    async def update(self, resource: str, data: dict, part: list = [], **kwargs):
        
        query_type = parse_resource(resource)
        endpoint = build_endpoint(query_type=query_type, key=self._key, part=part, **kwargs)
        
        result = await self._session.put(endpoint=endpoint, data=json.dumps(data), 
            headers={'Authorization': 'Bearer {}'.format(self._token),
                'Content-Type': 'application/json'})

        return YouTubeAPIResponse(await result.json(), result.status)

    async def rate(self, resource: str, rating: str, **kwargs):
        
        if rating not in RATINGS:
            raise ValueError('rating argument must be one of %r' % list(RATINGS))
        
        query_type = parse_resource(resource)
        query_type += '/rate'

        endpoint = build_endpoint(query_type=query_type, key=self._key, rating=rating, **kwargs)

        result = await self._session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})

        return YouTubeAPIResponse(await result.json(), result.status)

    async def getRating(self, resource: str, **kwargs):
        
        query_type = parse_resource(resource)
        query_type += '/getRating'

        endpoint = build_endpoint(query_type=query_type, key=self._key, **kwargs)

        result = await self._session.get(endpoint=endpoint, 
            headers={'Authorization': 'Bearer {}'.format(self._token)})

        return YouTubeAPIResponse(await result.json(), result.status)
        
    async def reportAbuse(self, resource: str, data: dict, **kwargs):
        
        query_type = parse_resource(resource)
        query_type += '/reportAbuse'

        endpoint = build_endpoint(query_type=query_type, key=self._key, **kwargs)

        result = await self._session.post(endpoint=endpoint, data=data,
            headers={'Authorization': 'Bearer {}'.format(self._token)})

        return YouTubeAPIResponse(await result.json(), result.status)

    async def delete(self, resource: str, **kwargs):

        query_type = parse_resource(resource)
        endpoint = build_endpoint(query_type=query_type, key=self._key, **kwargs)

        result = await self._session.delete(endpoint=endpoint, 
            headers={'Authorization': 'Bearer {}'.format(self._token)})

        return YouTubeAPIResponse(await result.json(), result.status)

    async def set_(self, resource: str, data: bytes, **kwargs):

        query_type = parse_resource(resource)
        query_type += '/set'
        
        endpoint = build_endpoint(query_type=query_type, key=self._key, **kwargs)
        url = 'https://www.googleapis.com/upload/youtube/v3/' + endpoint

        result = await self._session.post(endpoint=url, data=data,
            headers={'Authorization': 'Bearer {}'.format(self._token),
                'Content-Type': 'application/octet-stream',
                'Content-Length': str(len(data))})

        return YouTubeAPIResponse(await result.json(), result.status)

    async def unset(self, resource: str, **kwargs):

        query_type = parse_resource(resource)
        query_type += '/unset'

        endpoint = build_endpoint(query_type=query_type, key=self._key,  **kwargs)

        result = await self._session.post(endpoint=endpoint)

        return YouTubeAPIResponse(await result.json(), result.status)

    async def download(self, resource: str, **kwargs):
        
        query_type = parse_resource(resource)
        query_type += '/download'

        endpoint = build_endpoint(query_type=query_type, key=self._key, **kwargs)

        result = await self._session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})
        
        return YouTubeAPIResponse(await result.json(), result.status)

    async def markAsSpam(self, resource: str, **kwargs):

        query_type = parse_resource(resource)
        query_type += '/markAsSpam'

        endpoint = build_endpoint(query_type=query_type, key=self._key, **kwargs)

        result = await self._session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})

        return YouTubeAPIResponse(await result.json(), result.status)

    async def setModerationStatus(self, resource: str, **kwargs):

        query_type = parse_resource(resource)
        query_type += '/setModerationStatus'

        endpoint = build_endpoint(query_type=query_type, key=self._key, **kwargs)

        result = await self._session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})

        return YouTubeAPIResponse(await result.json(), result.status)


class YouTubeCrossClient(YouTubeAuthClient, YouTubeBaseClient):

    """
        Client object for making YouTube API requests with or w/o an access token.
        
        Use this client when you need the functionality of the base and authorized
        client class.
        
        Parent(s):
            YouTubeAuthClient
            YouTubeBaseClient
        
        Attribute(s):
            key type(str): YouTube API key 
            token type(str): Access token
    """

    def __init__(self, key: str, token: str):
        super().__init__(key, token)

    async def list_(self, resource: str, part: str, auth: bool = True, **kwargs):
        if auth:
            return await super().list_(resource, part, **kwargs)
        else:
            return await YouTubeBaseClient.list_(self, resource, part, **kwargs)
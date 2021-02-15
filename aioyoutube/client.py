import asyncio
import aiohttp
import json
from asyncio import AbstractEventLoop
from aiohttp import ClientSession

from .http import YouTubeAPISession, YouTubeAPIResponse
from .parse import build_endpoint
from .valid import RATINGS
from .exceptions import find_http_exception


class YouTubeAPIClient:

    """
        Base client object for the YouTube Data API with basic connection functionality.

        An object of this class should not be directly initialized.
        
        Parent(s):
            None
        
        Attribute(s):
            key type(str): YouTube API key
            exceptions type(bool): flag turning on or off library specific exceptions
    """

    def __init__(self, key: str, exceptions: bool = False):

        self._key = key
        self._exceptions = exceptions
        self._session = None

    @classmethod
    def from_connect(cls, key: str, exceptions: bool = False, loop: AbstractEventLoop = None):
        
        class_ = cls(key, exceptions)
        loop_ = loop or asyncio.get_event_loop()
        class_._session = YouTubeAPISession(loop=loop_)
        return class_

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value: str):
        self._key = value

    def connect(self, loop: AbstractEventLoop = None):
        
        loop_ = loop or asyncio.get_event_loop()
        self._session = YouTubeAPISession(loop=loop_)

    async def close(self):
        await self._session.close()


class YouTubeClient(YouTubeAPIClient):
    
    """
        Client object for making YouTube API requests w/o an access token.
        
        Use this client when you are wanting to access less sensitive data 
        from the YouTube Data API such as gathering public video data.
        
        Parent(s):
            YouTubeAPIClient
        
        Attribute(s):
            key type(str): YouTube API key 
            exceptions type(bool): flag turning on or off library specific exceptions
    """

    def __init__(self, key: str, exceptions: bool = False):
        super().__init__(key, exceptions)

    async def search(self, search: str, **kwargs):
        return await self.list_(resource='search', part=['snippet'], 
            q=search, **kwargs)        

    async def list_(self, resource, part: list, **kwargs):

        endpoint = build_endpoint(resource=resource, key=self._key, part=part, **kwargs)
        result = await self._session.get(endpoint=endpoint)

        if self._exceptions == True: await find_http_exception(result)
        return YouTubeAPIResponse(await result.json(), result.status, None)


class YouTubeAuthClient(YouTubeAPIClient):

    """
        Client object for making YouTube API requests with an access token.
        
        Use this client when you are wanting access to sensitive information
        and/or implementing actions such as liking a video.
        
        Parent(s):
            YouTubeAPIClient
        
        Attribute(s):
            key type(str): YouTube API key
            token type(str): OAuth2 Access token
            exceptions type(bool): flag turning on or off library specific exceptions
    """

    def __init__(self, key: str, token: str, exceptions: bool = False):
        self._token = token
        super().__init__(key, exceptions)
    
    @classmethod
    def from_token_connect(cls, key: str, token: str, exceptions: bool = False, loop: AbstractEventLoop = None):
        
        class_ = cls(key, token, exceptions)
        loop_ = loop or asyncio.get_event_loop()
        class_._session = YouTubeAPISession(loop=loop_)
        return class_

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value: str):
        self._token = value

    async def list_(self, resource: str, part: list, **kwargs):

        endpoint = build_endpoint(resource=resource, key=self._key, part=part, **kwargs)
        result = await self._session.get(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})

        if self._exceptions == True: await find_http_exception(result)
        return YouTubeAPIResponse(await result.json(), result.status, None)

    async def insert(self, resource: str, data: dict, media: bytes = None, part: list = [], method: str = None, **kwargs):
        
        endpoint = build_endpoint(resource=resource, key=self._key, part=part, method=method, **kwargs)
        
        if media != None:
            with aiohttp.MultipartWriter('form-data') as mpw:
                mpw.append_json(data)
                mpw.append(media, {'Content-Type': 'application/octet-stream'})
                
                result = await self._session.post(endpoint=endpoint, data=mpw, upload=True,
                    headers={'Authorization': 'Bearer {}'.format(self._token)})

                if self._exceptions == True: await find_http_exception(result) 
                return YouTubeAPIResponse(await result.json(), result.status, None)
        else:
            result = await self._session.post(endpoint=endpoint, data=json.dumps(data),
                headers={'Authorization': 'Bearer {}'.format(self._token)})
            
            if self._exceptions == True: await find_http_exception(result)
            return YouTubeAPIResponse(await result.json(), result.status, None)

    async def update(self, resource: str, data: dict, part: list = [], **kwargs):
        
        endpoint = build_endpoint(resource=resource, key=self._key, part=part, **kwargs)
        result = await self._session.put(endpoint=endpoint, data=json.dumps(data), 
            headers={'Authorization': 'Bearer {}'.format(self._token),
                'Content-Type': 'application/json'})

        if self._exceptions == True: await find_http_exception(result)
        return YouTubeAPIResponse(await result.json(), result.status, None)

    async def rate(self, resource: str, rating: str, **kwargs):
        
        if rating not in RATINGS:
            raise ValueError('rating argument must be one of %r' % list(RATINGS))

        endpoint = build_endpoint(resource=resource, key=self._key, method='rate', rating=rating, **kwargs)
        result = await self._session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})
        
        if self._exceptions == True: await find_http_exception(result)
        return YouTubeAPIResponse(await result.json(), result.status, None)

    async def getRating(self, resource: str, **kwargs):
        
        endpoint = build_endpoint(resource=resource, key=self._key, method='getRating', **kwargs)
        result = await self._session.get(endpoint=endpoint, 
            headers={'Authorization': 'Bearer {}'.format(self._token)})
        
        if self._exceptions == True: await find_http_exception(result)
        return YouTubeAPIResponse(await result.json(), result.status, None)
        
    async def reportAbuse(self, resource: str, data: dict, **kwargs):
        
        endpoint = build_endpoint(resource=resource, key=self._key, method='reportAbuse' **kwargs)
        result = await self._session.post(endpoint=endpoint, data=data,
            headers={'Authorization': 'Bearer {}'.format(self._token)})
        
        if self._exceptions == True: await find_http_exception(result)
        return YouTubeAPIResponse(await result.json(), result.status, None)

    async def delete(self, resource: str, **kwargs):

        endpoint = build_endpoint(resource=resource, key=self._key, **kwargs)
        result = await self._session.delete(endpoint=endpoint, 
            headers={'Authorization': 'Bearer {}'.format(self._token)})
        
        if self._exceptions == True: await find_http_exception(result)
        return YouTubeAPIResponse(await result.json(), result.status, None)

    async def set_(self, resource: str, data: bytes, **kwargs):

        endpoint = build_endpoint(resource=resource, key=self._key, method='set', **kwargs)
        result = await self._session.post(endpoint=endpoint, data=data, upload=True,
            headers={'Authorization': 'Bearer {}'.format(self._token),
                'Content-Type': 'application/octet-stream',
                'Content-Length': str(len(data))})

        if self._exceptions == True: await find_http_exception(result)
        return YouTubeAPIResponse(await result.json(), result.status, None)

    async def unset(self, resource: str, **kwargs):

        endpoint = build_endpoint(resource=resource, key=self._key, method='unset', **kwargs)
        result = await self._session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})

        if self._exceptions == True: await find_http_exception(result)
        return YouTubeAPIResponse(await result.json(), result.status, None)

    async def download(self, resource: str, method: str = None, **kwargs):

        endpoint = build_endpoint(resource=resource, key=self._key, method=method, **kwargs)
        result = await self._session.get(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})

        # this is necessary because in a good request, the returned content will only be binary data and
        # causes an exception if you try to call the json() coroutine

        try:
            if self._exceptions == True: await find_http_exception(result)
            return YouTubeAPIResponse(await result.json(), result.status, await result.read())
        except:
            return YouTubeAPIResponse(None, result.status, await result.read())

    async def markAsSpam(self, resource: str, **kwargs):

        endpoint = build_endpoint(resource=resource, key=self._key, method='markAsSpam' **kwargs)
        result = await self._session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})

        if self._exceptions == True: await find_http_exception(result)
        return YouTubeAPIResponse(await result.json(), result.status, None)

    async def setModerationStatus(self, resource: str, **kwargs):

        endpoint = build_endpoint(resource=resource, key=self._key, method='setModerationStatus' **kwargs)
        result = await self._session.post(endpoint=endpoint, headers={
            'Authorization': 'Bearer {}'.format(self._token)})

        if self._exceptions == True: await find_http_exception(result)
        return YouTubeAPIResponse(await result.json(), result.status, None)


class YouTubeHybridClient(YouTubeAuthClient, YouTubeClient):

    """
        Client object for making YouTube API requests with or w/o an access token.
        
        Use this client when you need the functionality of the base and authorized
        client class.
        
        Parent(s):
            YouTubeAuthClient
            YouTubeClient
        
        Attribute(s):
            key type(str): YouTube API key 
            token type(str): Access token
            exceptions type(bool): flag turning on or off library specific exceptions
    """

    def __init__(self, key: str, token: str, exceptions: bool = False):
        super().__init__(key, token, exceptions)

    async def list_(self, resource: str, part: str, auth: bool = True, **kwargs):
        if auth:
            return await super().list_(resource, part, **kwargs)
        else:
            return await YouTubeClient.list_(self, resource, part, **kwargs)
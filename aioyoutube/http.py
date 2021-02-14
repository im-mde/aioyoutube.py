import asyncio
from typing import Any
from asyncio import AbstractEventLoop
from aiohttp import ClientSession
from aiohttp.typedefs import StrOrURL
from aiohttp.client_exceptions import InvalidURL


BASE_URL = 'https://www.googleapis.com/youtube/v3/'
UPLOAD_URL = 'https://www.googleapis.com/upload/youtube/v3/'


class YouTubeAPISession():

    """
        Represents an HTTP client session to the YouTube Data API.

        This does not need to be directly initialized unless you want
        to directly control your HTTP requests with this class. 

        Parent(s):
            None

        Attribute(s):
            base_url type(str): base url pointing to the YouTube Data API w/o an endpoint
            upload_url type(str): url pointing to the upload portion of the YouTube Data API 
    """

    def __init__(self, loop: AbstractEventLoop = None, base_url: str = None, upload_url: str = None, **kwargs):

        loop_ = loop or asyncio.get_event_loop()
        self._session = ClientSession(loop=loop_, **kwargs)
        self.base_url = base_url or BASE_URL
        self.upload_url = upload_url or UPLOAD_URL

    async def get(self, endpoint: StrOrURL, *, allow_redirects: bool = True, **kwargs):

        if 'https://www.googleapis.com' not in endpoint:
            return await self._session.get(url=self.base_url + endpoint, allow_redirects=allow_redirects, **kwargs)
        else:
            return await self._session.get(url=endpoint, allow_redirects=allow_redirects, **kwargs)
        
    async def put(self, endpoint: StrOrURL, *, data: Any = None, **kwargs: Any):
        
        if 'https://www.googleapis.com' not in endpoint:
            return await self._session.put(url=self.base_url + endpoint, data=data, **kwargs)
        else:
            return await self._session.put(url=endpoint, data=data)

    async def post(self, endpoint: StrOrURL, * , data: Any = None, upload: bool = False, **kwargs: Any):

        if 'https://www.googleapis.com' not in endpoint:
            if upload:
                return await self._session.post(url=self.upload_url + endpoint, data=data, **kwargs)
            else:
                return await self._session.post(url=self.base_url + endpoint, data=data, **kwargs)
        else:
            return await self._session.post(url=endpoint, data=data, **kwargs)

    async def delete(self, endpoint: StrOrURL, **kwargs: Any):
        
        if 'https://www.googleapis.com' not in endpoint:
            return await self._session.delete(url=self.base_url + endpoint, **kwargs)
        else:
            return await self._session.post(url=endpoint, **kwargs)

    async def close(self):
        if not self._session.closed:
            await self._session.close()


class YouTubeAPIResponse:

    """
        Object for an http response from the YouTube Data API

        All client coroutines will return this object that encapsulates
        any json or binary data in addition to the http status code.

        Parent(s):
            None

        Attribute(s):
            json type(dict): json returned from an http request
            status type(int): http response status code for http request
            data type(bytes): binary data returned from http request
    """

    def __init__(self, json: dict, status: int, data: bytes = None):
        
        self._json = json
        self._status = status
        self._data = data
    
    @property
    def json(self):
        return self._json

    @property
    def status(self):
        return self._status
    
    @property
    def data(self):
        return self._data
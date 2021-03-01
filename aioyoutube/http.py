import asyncio

from typing import Any, Optional, MutableMapping, Tuple, Union
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

    def __init__(
        self, 
        loop: AbstractEventLoop = None, 
        base_url: str = None, 
        upload_url: str = None, 
        **kwargs
    ) -> None:

        loop_ = loop or asyncio.get_event_loop()
        self._session = ClientSession(loop=loop_, **kwargs)
        self.base_url = base_url or BASE_URL
        self.upload_url = upload_url or UPLOAD_URL

    async def _determine_url(self, upload: bool) -> str:

        if upload:
            return UPLOAD_URL
        else:
            return BASE_URL

    async def request(
        self, 
        method: str, 
        endpoint: str,
        upload: bool = False, 
        headers: Optional[MutableMapping] = None,
        body: Optional[Union[MutableMapping, bytes]] = None,
    ) -> Tuple[int, bytes, MutableMapping]:
        
        url = await self._determine_url(upload) + endpoint

        async with self._session.request(
            method, url, headers=headers, data=body) as response:
                return response.status, await response.read(), response.headers

    async def close(self) -> bool:
        
        if not self._session.closed:
            await self._session.close()
            return True
        else:
            return False


class YouTubeAPIResponse:

    """
        Object for an http response from the YouTube Data API

        All client coroutines will return this object that encapsulates
        any json or binary data in addition to the http status code.

        Parent(s):
            None

        Attribute(s):
            status type(int): http response status code for http request
            data type(Union[MutableMapping, bytes]): data returned from http request
            headers type(MutableMapping): headers returned from http request
    """

    def __init__(
        self, 
        status: int, 
        data: Union[MutableMapping, bytes], 
        headers: MutableMapping
    ) -> None:
        
        self._status = status
        self._data = data
        self._headers = headers
    
    @property
    def data(self) -> [MutableMapping, bytes]:
        return self._data

    @property
    def status(self) -> int:
        return self._status
    
    @property
    def headers(self) -> MutableMapping:
        return self._headers
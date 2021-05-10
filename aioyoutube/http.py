"""

The MIT License (MIT)

Copyright (c) 2021 im-mde

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

"""


import asyncio
import aiohttp
from typing import Any, Optional, MutableMapping, Tuple, Union
from aiohttp import ClientSession


BASE_URL = 'https://www.googleapis.com/youtube/v3/'
UPLOAD_URL = 'https://www.googleapis.com/upload/youtube/v3/'

# TODO: Add context manager to support case where user wants to directly initialize YouTubeAPISession
class YouTubeAPISession:

    """
        Represents an HTTP client session to the YouTube Data API.

        This does not need to be directly initialized unless you want
        to directly control your HTTP requests with this class. 

        Parent(s):
            None

        Attribute(s):
            session type(aiohttp.ClientSession): async http session from aiohttp library
    """

    def __init__(self, session: aiohttp.ClientSession = None, **kwargs) -> None:        
        self._session = session or ClientSession(**kwargs)

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
        the HTTP status code, returned data, and headers.

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
    def data(self) -> Union[MutableMapping, bytes]:
        return self._data

    @property
    def status(self) -> int:
        return self._status
    
    @property
    def headers(self) -> MutableMapping:
        return self._headers
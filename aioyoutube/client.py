import aiohttp, json, ast
from aiohttp import ClientSession
from typing import Optional, MutableMapping
from .http import YouTubeAPISession, YouTubeAPIResponse
from .parse import build_endpoint
from .valid import RATINGS
from .exceptions import (
    is_http_exception, 
    RatingInvalidException,
    ResourceInvalidException,
    YouTubeKeyNoneException,
    OAuthTokenNoneException
)

class YouTubeAPIClient:

    """
        Base client object for the YouTube Data API with basic connection functionality.

        An object of this class should not be directly initialized.
        
        Parent(s):
            None
        
        Attribute(s):
            key type(str): YouTube API key
            http_exceptions type(bool): flag turning on or off http specific exceptions
            session type(aiohttp.ClientSession): async http session from aiohttp library
    """

    def __init__(self, key: str, http_exceptions: bool = False) -> None:

        if key == None:
            raise YouTubeKeyNoneException

        self._key = key
        self._exceptions = http_exceptions
        self._session = None

    @classmethod
    def from_connect(
        cls, 
        key: str, 
        http_exceptions: bool = False, 
        session: aiohttp.ClientSession = None
    ) -> classmethod:
        
        class_ = cls(key, http_exceptions)
        session_ = session or ClientSession()
        class_._session = YouTubeAPISession(session=session_)
        return class_

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, value: str) -> None:
        self._key = value

    def connect(self, session: aiohttp.ClientSession = None) -> None:

        session_ = session or ClientSession()
        self._session = YouTubeAPISession(session=session_)

    async def close(self) -> None:
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
            http_exceptions type(bool): flag turning on or off http specific exceptions
            session type(aiohttp.ClientSession): async http session from aiohttp library
    """

    def __init__(self, key: str, http_exceptions: bool = False) -> None:
        super().__init__(key, http_exceptions)

    async def search(self, search: str, **kwargs) -> YouTubeAPIResponse:
        return await self.list_(resource='search', part=['snippet'], 
            q=search, **kwargs)        

    async def list_(
        self, 
        resource: str, 
        part: list, 
        **kwargs
    ) -> YouTubeAPIResponse:

        endpoint = build_endpoint(resource=resource, key=self._key, 
            part=part, **kwargs)
        result = await self._session.request(method='GET', endpoint=endpoint)

        data = ast.literal_eval(result[1].decode('UTF8'))
        if self._exceptions == True: 
            await is_http_exception(result[0], data)

        return YouTubeAPIResponse(result[0], data, result[2])


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
            http_exceptions type(bool): flag turning on or off http specific exceptions
            session type(aiohttp.ClientSession): async http session from aiohttp library
    """

    def __init__(
        self, 
        key: str, 
        token: str, 
        http_exceptions: bool = False
    ) -> None:

        if token == None:
            raise OAuthTokenNoneException
        
        self._token = token
        super().__init__(key, http_exceptions)
    
    @classmethod
    def from_token_connect(
        cls, 
        key: str, 
        token: str, 
        http_exceptions: bool = False, 
        session: aiohttp.ClientSession = None
    ) -> classmethod:
        
        class_ = cls(key, token, http_exceptions)
        session_ = session or ClientSession()
        class_._session = YouTubeAPISession(session=session_)
        return class_

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, value: str) -> None:
        self._token = value

    async def list_(
        self, 
        resource: str, 
        part: list, 
        **kwargs
    ) -> YouTubeAPIResponse:

        endpoint = build_endpoint(resource=resource, key=self._key, 
            part=part, **kwargs)
        
        result = await self._session.request(
            method='GET', 
            endpoint=endpoint,
            headers={'Authorization': 'Bearer {}'.format(self._token)}
        )

        data = ast.literal_eval(result[1].decode('UTF8'))
        if self._exceptions == True: 
            await is_http_exception(result[0], data)
        return YouTubeAPIResponse(result[0], data, result[2])

    async def insert(
        self, 
        resource: str, 
        data: dict, 
        media: Optional[bytes] = None, 
        part: Optional[list] = [], 
        method: Optional[str] = None, 
        **kwargs
    ) -> YouTubeAPIResponse:
        
        endpoint = build_endpoint(resource=resource, key=self._key, 
            part=part, method=method, **kwargs)
        
        if media == None:
            
            result = await self._session.request(
                method='POST',
                endpoint=endpoint,
                headers={'Authorization': 'Bearer {}'.format(self._token)},
                body=json.dumps(data)
            )

            data = ast.literal_eval(result[1].decode('UTF8'))
            if self._exceptions == True: 
                await is_http_exception(result[0], data)
            return YouTubeAPIResponse(result[0], data, result[2])
        else:
            with aiohttp.MultipartWriter('form-data') as mpw:
                mpw.append_json(data)
                mpw.append(media, {'Content-Type': 'application/octet-stream'})

                result = await self._session.request(
                    method='POST',
                    endpoint=endpoint,
                    upload=True,
                    headers={'Authorization': 'Bearer {}'.format(self._token)},
                    body=mpw
                )

                # TODO: look at why this is not decoding. will be commented out for now
                #data = ast.literal_eval(result[1].decode('UTF8'))
                if self._exceptions == True: 
                    await is_http_exception(result[0], result[1])
                return YouTubeAPIResponse(result[0], result[1], result[2])

    async def update(
        self, 
        resource: str, 
        data: MutableMapping, 
        part: Optional[list] = [], 
        **kwargs
    ) -> YouTubeAPIResponse:
        
        endpoint = build_endpoint(resource=resource, key=self._key, part=part, **kwargs)
        
        result = await self._session.request(
            method='PUT', 
            endpoint=endpoint, 
            body=json.dumps(data), 
            headers={'Authorization': 'Bearer {}'.format(self._token)}
        )

        data = ast.literal_eval(result[1].decode('UTF8'))
        if self._exceptions == True: 
            await is_http_exception(result[0], data)
        return YouTubeAPIResponse(result[0], data, result[2])

    async def rate(
        self, 
        resource: str, 
        rating: str, 
        **kwargs
    ) -> YouTubeAPIResponse:
        
        if rating not in RATINGS:
            raise RatingInvalidException
        
        endpoint = build_endpoint(resource=resource, key=self._key, method='rate', rating=rating, **kwargs)
        
        result = await self._session.request(
            method='POST', 
            endpoint=endpoint, 
            headers={'Authorization': 'Bearer {}'.format(self._token), 
                'Accept': 'application/json'}
        )
 
        if self._exceptions == True: 
            await is_http_exception(result[0], result[1])
        return YouTubeAPIResponse(result[0], None, result[2])

    async def getRating(self, resource: str, **kwargs) -> YouTubeAPIResponse:
        
        endpoint = build_endpoint(resource=resource, key=self._key, method='getRating', **kwargs)

        result = await self._session.request(
            method='GET',
            endpoint=endpoint,
            headers={'Authorization': 'Bearer {}'.format(self._token)}
        )
        
        data = ast.literal_eval(result[1].decode('UTF8'))
        if self._exceptions == True: 
            await is_http_exception(result[0], data)
        return YouTubeAPIResponse(result[0], data, result[2])
        
    async def reportAbuse(
        self, 
        resource: str, 
        data: MutableMapping, 
        **kwargs
    ) -> YouTubeAPIResponse:
        
        endpoint = build_endpoint(resource=resource, key=self._key, method='reportAbuse' **kwargs)

        result = await self._session.request(
            method='POST',
            endpoint=endpoint,
            body=json.dumps(data),
            headers={'Authorization': 'Bearer {}'.format(self._token)},
        )
        
        if self._exceptions == True: 
            await is_http_exception(result[0], result[1])
        return YouTubeAPIResponse(result[0], None, result[2])

    async def delete(self, resource: str, **kwargs) -> YouTubeAPIResponse:

        endpoint = build_endpoint(resource=resource, key=self._key, **kwargs)

        result = await self._session.request(
            method='DELETE',
            endpoint=endpoint,
            headers={'Authorization': 'Bearer {}'.format(self._token)}
        )

        if self._exceptions == True: 
            await is_http_exception(result[0], result[1])
        return YouTubeAPIResponse(result[0], None, result[2])

    async def set_(
        self, 
        resource: str, 
        data: bytes, 
        **kwargs
    ) -> YouTubeAPIResponse:

        endpoint = build_endpoint(resource=resource, key=self._key, method='set', **kwargs)

        result = await self._session.request(
            method='POST',
            endpoint=endpoint,
            upload=True,
            headers={'Authorization': 'Bearer {}'.format(self._token),
                'Content-Type': 'application/octet-stream'},
            body=data
        )

        data = ast.literal_eval(result[1].decode('UTF8'))
        if self._exceptions == True: 
            await is_http_exception(result[0], data)
        return YouTubeAPIResponse(result[0], data, result[2])

    async def unset(self, resource: str, **kwargs) -> YouTubeAPIResponse:

        endpoint = build_endpoint(resource=resource, key=self._key, method='unset', **kwargs)

        result = await self._session.request(
            method='POST',
            endpoint=endpoint,
            upload=True,
            headers={'Authorization': 'Bearer {}'.format(self._token)}
        )

        if self._exceptions == True: 
            await is_http_exception(result[0], result[1])
        return YouTubeAPIResponse(result[0], None, result[2])

    async def download(
        self, 
        resource: str, 
        method: Optional[str] = None,
        **kwargs
    ) -> YouTubeAPIResponse:

        endpoint = build_endpoint(resource=resource, key=self._key, method=method, **kwargs)

        result = await self._session.request(
            method='GET',
            endpoint=endpoint,
            headers={'Authorization': 'Bearer {}'.format(self._token)}
        )

        if self._exceptions == True: 
            await is_http_exception(result[0], result[1])
        return YouTubeAPIResponse(result[0], result[1], result[2])

    async def markAsSpam(self, resource: str, **kwargs) -> YouTubeAPIResponse:

        endpoint = build_endpoint(resource=resource, key=self._key, method='markAsSpam' **kwargs)

        result = await self._session.request(
            method='POST',
            endpoint=endpoint,
            headers={'Authorization': 'Bearer {}'.format(self._token)}
        )

        if self._exceptions == True: 
            await is_http_exception(result[0], result[1])
        return YouTubeAPIResponse(result[0], None, result[2])

    async def setModerationStatus(
        self, 
        resource: str, 
        **kwargs
    ) -> YouTubeAPIResponse:

        endpoint = build_endpoint(resource=resource, key=self._key, method='setModerationStatus' **kwargs)

        result = await self._session.request(
            method='POST',
            endpoint=endpoint,
            headers={'Authorization': 'Bearer {}'.format(self._token)}
        )

        if self._exceptions == True: 
            await is_http_exception(result[0], result[1])
        return YouTubeAPIResponse(result[0], None, result[2])


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
            http_exceptions type(bool): flag turning on or off http specific exceptions
            session type(aiohttp.ClientSession): async http session from aiohttp library
    """

    def __init__(
        self, 
        key: str, 
        token: str, 
        http_exceptions: bool = False
    ) -> None:
        super().__init__(key, token, http_exceptions)

    async def list_(
        self, 
        resource: str, 
        part: list, 
        auth: bool = True, 
        **kwargs
    ) -> YouTubeAPIResponse:
        
        if auth:
            return await super().list_(resource, part, **kwargs)
        else:
            return await YouTubeClient.list_(self, resource, part, **kwargs)
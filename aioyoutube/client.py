from asyncio import AbstractEventLoop
from aiohttp import ClientSession
from aioyoutube.http import YouTubeAPISession
import asyncio

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

def build_endpoint(query_type: str, part: list, key: str, **kwargs):
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

    def __init__(self, key: str, loop: AbstractEventLoop = None, session: YouTubeAPISession = None):
        self.key = key
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or YouTubeAPISession()

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
        query_type = parse_kind(kind)
        endpoint = build_endpoint(query_type, part, self.key, **kwargs)
        result = await self.session.get(endpoint=endpoint)
        
        if not json:
            pass
        else:
            return await result.json()

    async def download(self, part = None, **kwargs):
        NotImplemented
    
    async def close_session(self):
        await self.session.close()
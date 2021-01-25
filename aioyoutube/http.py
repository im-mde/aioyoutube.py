from typing import Any
from aiohttp import ClientSession
from aiohttp.typedefs import StrOrURL
from aiohttp.client_exceptions import InvalidURL

BASE_URL = 'https://www.googleapis.com/youtube/v3/'

# TODO: Implement this class w/o inheriting ClientSession. It's recommended not to inherit 
#       in favor of including a ClienSession object within your custom client class
class YouTubeAPISession(ClientSession):

    """
        Represents an async http session used to make http requests

        Parent(s):
            aiohttp.ClientSession

        Attribute(s):
            base_url type(str): base url pointing to the YouTube Data API w/o an endpoint

        Method(s):
            get ret(dict): makes an HTTP GET request to the YouTube Data API
            put ret(dict): makes an HTTP PUT request to the YouTube Data API
            post ret(dict): makes an HTTP POST request to the YouTube Data API
            delete ret(dict): makes an HTTP DELETE request to the YouTube Data API
    
    """

    def __init__(self, base_url: str = None, **kwargs):

        self.base_url = base_url or BASE_URL
        super().__init__(**kwargs)

    def get(self, endpoint: StrOrURL, *, allow_redirects: bool = True, **kwargs):

        if BASE_URL not in endpoint:
            url = self.base_url + endpoint
            return super().get(url=url, allow_redirects=allow_redirects, **kwargs)
        elif BASE_URL in endpoint:
            return super().get(url=endpoint, allow_redirects=allow_redirects, **kwargs)
        
    def put(self, endpoint: StrOrURL, *, data: Any = None, **kwargs: Any):
        
        if BASE_URL not in endpoint:
            url = self.base_url + endpoint
            return super().put(url=url, data=data, **kwargs)
        elif BASE_URL in endpoint:
            return super().put(url=endpoint, data=data)

    def post(self, endpoint: StrOrURL, * , data: Any = None, **kwargs: Any):
        
        if BASE_URL not in endpoint:
            url = self.base_url + endpoint
            return super().post(url=url, data=data, **kwargs)
        elif BASE_URL in endpoint:
            return super().post(url=endpoint, data=data, **kwargs)

    def delete(self, endpoint: StrOrURL, **kwargs: Any):
        
        if BASE_URL not in endpoint:
            url = self.base_url + endpoint
            return super().delete(url=url, **kwargs)
        elif BASE_URL in endpoint:
            return super().post(url=endpoint, **kwargs)

class YouTubeAPIResponse:

    def __init__(self, json: dict, status: int):
        
        self._json = json
        self._status = status
    
    @property
    def json(self):
        return self._json

    @property
    def status(self):
        return self._status
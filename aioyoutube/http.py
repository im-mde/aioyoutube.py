from typing import Any
from aiohttp import ClientSession
from aiohttp.typedefs import StrOrURL

BASE_URL = 'https://www.googleapis.com/youtube/v3/'

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
        try:
            url = self.base_url + endpoint
            return super().get(url=url, allow_redirects=allow_redirects, **kwargs)
        except:
            return super().get(url=endpoint, allow_redirects=allow_redirects, **kwargs)

    def put(self, endpoint: StrOrURL, *, data: Any = None, **kwargs: Any):
        try:
            url = self.base_url + endpoint
            return super().put(url=url, data=data, **kwargs)
        except:
            return super().put(url=endpoint, data=data, **kwargs)
    
    def post(self, endpoint: StrOrURL, * , data: Any = None, **kwargs: Any):
        try:
            url = self.base_url + endpoint
            return super().post(url=url, data=data, **kwargs)
        except:
            return super().post(url=endpoint, data=data, **kwargs)

    def delete(self, endpoint: StrOrURL, **kwargs: Any):
        try:
            url = self.base_url + endpoint
            return super().delete(url=url, **kwargs)
        except:
            return super().post(url=endpoint, **kwargs)
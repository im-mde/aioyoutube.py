from typing import Any
from aiohttp import ClientSession
from aiohttp.typedefs import StrOrURL
from aiohttp.client_exceptions import InvalidURL


BASE_URL = 'https://www.googleapis.com/youtube/v3/'
UPLOAD_URL = 'https://www.googleapis.com/upload/youtube/v3/'

# TODO: Implement this class w/o inheriting ClientSession. It's recommended not to inherit 
#       in favor of including a ClienSession object within your custom client class

class YouTubeAPISession(ClientSession):

    """
        Represents an HTTP client session to the YouTube Data API.

        This does not need to be directly initialized unless you want
        to directly control your HTTP requests with this class. 

        Parent(s):
            aiohttp.ClientSession

        Attribute(s):
            base_url type(str): base url pointing to the YouTube Data API w/o an endpoint
            upload_url type(str): url pointing to the upload portion of the YouTube Data API 
    """

    def __init__(self, base_url: str = None, upload_url: str = None, **kwargs):

        self.base_url = base_url or BASE_URL
        self.upload_url = upload_url or UPLOAD_URL
        super().__init__(**kwargs)

    def get(self, endpoint: StrOrURL, *, allow_redirects: bool = True, **kwargs):

        if 'https://www.googleapis.com' not in endpoint:
            return super().get(url=self.base_url + endpoint, allow_redirects=allow_redirects, **kwargs)
        else:
            return super().get(url=endpoint, allow_redirects=allow_redirects, **kwargs)
        
    def put(self, endpoint: StrOrURL, *, data: Any = None, **kwargs: Any):
        
        if 'https://www.googleapis.com' not in endpoint:
            return super().put(url=self.base_url + endpoint, data=data, **kwargs)
        else:
            return super().put(url=endpoint, data=data)

    def post(self, endpoint: StrOrURL, * , data: Any = None, upload: bool = False, **kwargs: Any):

        if 'https://www.googleapis.com' not in endpoint:
            if upload:
                return super().post(url=self.upload_url + endpoint, data=data, **kwargs)
            else:
                return super().post(url=self.base_url + endpoint, data=data, **kwargs)
        else:
            return super().post(url=endpoint, data=data, **kwargs)

    def delete(self, endpoint: StrOrURL, **kwargs: Any):
        
        if 'https://www.googleapis.com' not in endpoint:
            url = self.base_url + endpoint
            return super().delete(url=url, **kwargs)
        else:
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
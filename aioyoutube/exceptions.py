from .http import YouTubeAPIResponse
from .valid import get_youtube_resources, get_ratings

async def find_http_exception(response: YouTubeAPIResponse):
    
    if response.status == 400: 
        raise YouTubeBadRequestException(response.status, await response.json())
    elif response.status == 401:
        raise YouTubeUnauthorizedException(response.status, await response.json())
    elif response.status == 403:
        raise YouTubeForbiddenException(response.status, await response.json())
    elif response.status == 404:
        raise YouTubeNotFoundException(response.status, await response.json())
    elif response.status >= 400:
        raise YouTubeAPIHttpException(response.status, await response.json())
    else: return


class YouTubeAPIHttpException(Exception):

    """
        Generic HTTP exception for the YouTube Data API.
        
        This exception will be directly raised if the response code is greater than or
        equal to 400 and is not corresponding with one of its child exceptions.

        Parent(s):
            Exception
        
        Attribute(s):
            code type(int): status code of http response
            json type(dict): json of http response
    """

    def __init__(self, code: int, json: dict):
        self.message = 'Status Code {}: {}'.format(str(code), json['error']['message'])
        super().__init__(self.message)


class YouTubeUnauthorizedException(YouTubeAPIHttpException):

    """
        HTTP exception corresponding to a YouTube Data API response code 401.
        
        This exception will be directly raised if the response code is 401 which can
        occur when using a youtube user specific parameter or resource without properly 
        authenticating.

        Parent(s):
            YouTubeAPIHttpException
        
        Attribute(s):
            code type(int): status code of http response
            json type(dict): json of http response
    """

    def __init__(self, code: int, json: dict, **kwargs):
        super().__init__(code, json)


class YouTubeBadRequestException(YouTubeAPIHttpException):

    """
        HTTP exception corresponding to a YouTube Data API response code 400.
        
        This exception will be directly raised if the response code is 400 which can
        occur when not utilizing parameters properly for a certain request.

        Parent(s):
            YouTubeAPIHttpException
        
        Attribute(s):
            code type(int): status code of http response
            json type(dict): json of http response
    """

    def __init__(self, code: int, json: dict, **kwargs):
        super().__init__(code, json)


class YouTubeNotFoundException(YouTubeAPIHttpException):

    """
        HTTP exception corresponding to a YouTube Data API response code 404.
        
        This exception will be directly raised if the response code is 404 which can
        occur when you are referencing a resource via an identifier that doesn't exist.

        Parent(s):
            YouTubeAPIHttpException
        
        Attribute(s):
            code type(int): status code of http response
            json type(dict): json of http response
    """

    def __init__(self, code: int, json: dict):
        super().__init__(code, json)


class YouTubeForbiddenException(YouTubeAPIHttpException):

    """
        HTTP exception corresponding to a YouTube Data API response code 403.
        
        This exception will be directly raised if the response code is 403 which can
        occur when accessing a resource without the proper authority.

        Parent(s):
            YouTubeAPIHttpException
        
        Attribute(s):
            code type(int): status code of http response
            json type(dict): json of http response
    """

    def __init__(self, code: int, json: dict):
        super().__init__(code, json)


class YouTubeResourceInvalidException(Exception):

    """
        Invalid YouTube resource exception.

        This exception will occur when a resource is not valid but was input into 
        the resource argument of a client method.

        Parent(s):
            Exception

        Attribute(s):
            None
    """

    def __init__(self):
        self.message = 'Resource argument must be one of: {}'.format(get_youtube_resources())
        super().__init__(self.message)


class YouTubeRatingInvalidException(Exception):

    """
        Invalid YouTube rating exception.

        This exception will occur when a rating value is not valid but was input
        into the rating argument of the "rate" method of the client.

        Parent(s):
            Exception

        Attribute(s):
            None
    """

    def __init__(self):
        self.message = 'Rating argument must be one of: {}'.format(get_ratings())
        super().__init__(self.message)
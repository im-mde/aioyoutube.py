import ast
from typing import Union, MutableMapping
from .http import YouTubeAPIResponse
from .valid import get_youtube_resources, get_ratings

async def is_http_exception(
    status: int, 
    data: Union[MutableMapping, bytes]
) -> None:

    if status < 200 or status >= 300:
        data_ = data
        if type(data_) == bytes:
            data_= ast.literal_eval(data_.decode('UTF8'))
            print(data_)
        raise HTTPException(status, data_)
    else:
        return

class HTTPException(Exception):

    """
        HTTP exception for the YouTube Data API.
        
        This exception is raised if the response status is not between 200 and 299.

        Parent(s):
            Exception

        Attribute(s):
            status type(int): status status of http response
            json type(MutableMapping): json of http response
    """

    def __init__(self, status: int, json: MutableMapping) -> None:
        
        self.message = 'Status {}: {}'.format(
            str(status), json['error']['message'])
        super().__init__(self.message)


class YouTubeAPIException(Exception):

    """
        Generic exception for errors related to the YouTube Data API.

        This exception occurs for API specific errors such as an invalid value
        for an argument in a client coroutine.

        Parent(s):
            Exception

        Attribute(s):
            message type(str): string displaying information about the error.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ResourceInvalidException(YouTubeAPIException):

    """
        Invalid YouTube resource exception.

        This exception occurs when a resource is not valid but is input into 
        the resource argument of a client class coroutine.

        Parent(s):
            YouTubeAPIException

        Attribute(s):
            None
    """

    def __init__(self) -> None:
        
        self.message = 'Resource argument must be one of: {}'.format(
            get_youtube_resources())
        super().__init__(self.message)


class RatingInvalidException(YouTubeAPIException):

    """
        Invalid YouTube rating exception.

        This exception occurs when a rating value is not valid but is input
        into the rating argument of the rate coroutine of a client class.

        Parent(s):
            YouTubeAPIException

        Attribute(s):
            None
    """

    def __init__(self) -> None:
        
        self.message = 'Rating argument must be one of: {}'.format(
            get_ratings())
        super().__init__(self.message)


class NoneValueException(Exception):

    """
        Generic None value exception.

        This exception occurs when a required client class attribute is set
        to None.

        Parent(s):
            Exception

        Attribute(s):
            None
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class YouTubeKeyNoneException(NoneValueException):

    """
        YouTube key None exception. 

        This exception occurs when the key is set to None instead
        of a string when initializing a client class.

        Parent(s):
            NoneValueException

        Attribute(s):
            None
    """

    def __init__(self) -> None:

        self.message = 'YouTube API key is set to "None"'
        super().__init__(self.message)


class OAuthTokenNoneException(NoneValueException):

    """
        Oauth token None exception. 

        This exception occurs when the OAuth token is set to None instead
        of a string when initializing a client class.

        Parent(s):
            YouTubeNoneValueException

        Attribute(s):
            None
    """

    def __init__(self) -> None:

        self.message = 'OAuth token is set to "None"'
        super().__init__(self.message)
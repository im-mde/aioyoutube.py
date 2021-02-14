from .http import YouTubeAPIResponse

async def find_exception(response: YouTubeAPIResponse):
    
    if response.status == 400: 
        raise YouTubeBadRequestException(response.status, await response.json())
    elif response.status == 402:
        raise YouTubeUnauthorizedException(response.status, await response.json())
    elif response.status == 403:
        raise YouTubeForbiddenException(response.status, await response.json())
    elif response.status == 404:
        raise YouTubeNotFoundException(response.status, await response.json())
    else: return


class YouTubeAPIHttpException(Exception):

    def __init__(self, code: int, json: dict):
        self.message = 'Status Code {}: {}'.format(str(code), json['error']['message'])
        super().__init__(self.message)


class YouTubeUnauthorizedException(YouTubeAPIHttpException):

    def __init__(self, code: int, json: dict, **kwargs):
        super().__init__(code, json)


class YouTubeBadRequestException(YouTubeAPIHttpException):

    def __init__(self, code: int, json: dict, **kwargs):
        super().__init__(code, json)


class YouTubeNotFoundException(YouTubeAPIHttpException):

    def __init__(self, code: int, json: dict):
        super().__init__(code, json)


class YouTubeForbiddenException(YouTubeAPIHttpException):

    def __init__(self, code: int, json: dict):
        super().__init__(code, json)
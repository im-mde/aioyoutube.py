from typing import Optional
from .valid import YOUTUBE_RESOURCES
from .exceptions import ResourceInvalidException


# takes youtube resource and returns the equivalent url resource

def parse_resource(
    resource: str, 
    method: Optional[str] = ''
) -> str:    

    resource_ = resource
    if 'youtube#' in resource:
        resource_ = resource.split('#')[1]
    
    if resource_ not in YOUTUBE_RESOURCES:
        raise ResourceInvalidException
        
    # "search" resource is a special case that doesn't convert to plural
    # ex. video -> videos but search -> search

    if resource_ == 'search': 
        return 'search'
    elif resource[-1] == 'y': 
        return resource_[0:-1] + 'ies'
    else: 
        return resource_ + 's'


# generates a youtube api url from a youtube resource, other required parameters, and key word arguments

def build_endpoint(
    resource: str, 
    key: str, 
    part: Optional[list] = [], 
    method: Optional[str] = None, 
    **kwargs
) -> str:
    
    resource = parse_resource(resource=resource)    
    if method != None: resource += '/' + method

    endpoint = '{}?'.format(resource)

    if len(part) > 0:
        part = ','.join(part)
        endpoint += 'part=' + part

    for key_, value in kwargs.items():
        endpoint += '&{}={}'.format(key_, str(value))
    
    # example of a generated endpoint:
    # ex. videos?part=snippet&id=dQw4w9WgXcQ&maxResults=50&key=[YOUR_API_KEY]

    return endpoint + '&key=' + key
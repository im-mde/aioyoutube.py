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
from .valid import YOUTUBE_RESOURCES

def parse_resource(resource: str):    

    resource_ = resource
    if 'youtube#' in resource:
        resource_ = resource.split('#')[1]
    
    if resource_ not in YOUTUBE_RESOURCES:
        raise ValueError('Kind argument must be one of: %r' % list(YOUTUBE_RESOURCES))
    
    # "search" resource is a special case that doesn't convert to plural
    # ex. video -> videos but search -> search

    if resource_ == 'search': 
        return 'search'
    elif resource[-1] == 'y': 
        return resource_[0:-1] + 'ies'
    else: 
        return resource_

def build_endpoint(query_type: str, key: str, part: list = [], **kwargs):
    
    endpoint = '{}?'.format(query_type)

    if len(part) > 0:
        part = ','.join(part)
        endpoint = '{}?part={}'.format(query_type, part)

    for key_, value in kwargs.items():
        endpoint += '&{}={}'.format(key_, str(value))
    
    # example of a generated endpoint:
    # ex. videos?part=snippet&id=dQw4w9WgXcQ&maxResults=50&key=[YOUR_API_KEY]

    return endpoint + '&key={}'.format(key)
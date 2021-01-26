from .valid import KINDS

def parse_kind(kind):    

    kind_ = kind
    if 'youtube#' in kind:
        kind_ = kind.split('#')[1]
    
    if kind_ not in KINDS:
        raise ValueError('Kind argument must be one of: %r' % list(KINDS))
    
    if kind_[-1] == 'y': 
        return kind_[0:-1] + 'ies'
    elif kind_ != 'search': 
        return kind_ + 's'
    else: 
        return kind_

def build_endpoint(query_type: str, key: str, part: list = [], **kwargs):
    
    endpoint = '{}?'.format(query_type)
    if len(part) > 0:
        part = ','.join(part)
        endpoint = '{}?part={}'.format(query_type, part)
    
    for key_, value in kwargs.items():
        endpoint += '&{}={}'.format(key_, str(value))
    
    return endpoint + '&key={}'.format(key)
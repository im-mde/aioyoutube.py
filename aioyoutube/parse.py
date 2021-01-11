from .valid import KINDS

def parse_kind(kind):
    # TODO: clean up the function
    
    kind = kind
    if 'youtube#' in kind:
        kind = kind.split('#')[1]

    if kind not in KINDS:
        raise ValueError('Kind argument must be one of: %r' % KINDS)
    if kind[-1] == 'y':
        return kind[0:-1] + 'ies'
    elif kind != 'search':
        return kind + 's'
    else:
        return kind

def build_endpoint(query_type: str, key: str, part: list = [], **kwargs):
    endpoint = '{}?'.format(query_type)
    if len(part) > 0:
        part = ','.join(part)
        endpoint = '{}?part={}'.format(query_type, part)
    
    for key_, value in kwargs.items():
        endpoint += '&{}={}'.format(key_, str(value))
    
    return endpoint + '&key={}'.format(key)

def build_data(**kwargs):
    # TODO: cleanup whatever parsing mess this is supposed to be lol

    data = {}
    for key_, value, in kwargs.items():
        if '_' in key_:
            split = key_.split('_')
            dict_str = ''
            for i, key__ in enumerate(split):
                if i + 1 == len(split):
                    dict_str = "{{'{}':'{}'}}".format(key__, value)
                    try:
                        data[split[i-1]].update(eval(dict_str))
                    except:
                        data.update(eval(dict_str))
                else:
                    if key__ not in data.keys():
                        dict_str = "{{'{}':{{}}}}".format(key__)
                        data.update(eval(dict_str))
        else:
            data.update({key_: value})
    return data
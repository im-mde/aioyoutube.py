RATINGS = frozenset({'like', 'dislike', 'none'})
KINDS = frozenset({
    'watermark',  
    'videoCategory',
    'video',
    'videoAbuseReportReason',
    'thumbnail',
    'subscription',
    'search',
    'playlist',
    'playlistItem',
    'membershipsLevel',
    'member',
    'i18nRegion',
    'i18nLanguage',
    'commentThread',
    'comment',
    'channelSection',
    'channel',
    'channelBanner',
    'caption',
    'activity'
})

def get_kind_values():
    return list(KINDS)

def get_rating_values():
    return list(RATINGS)
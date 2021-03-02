
# list of all valid ratings that can be utilized in this library

RATINGS = frozenset({'like', 'dislike', 'none'})


# list of all valid youtube resources than can be utilized in this library

YOUTUBE_RESOURCES = frozenset({
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

def get_youtube_resources() -> list:
    return list(YOUTUBE_RESOURCES)

def get_ratings() -> list:
    return list(RATINGS)
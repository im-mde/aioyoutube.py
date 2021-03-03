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
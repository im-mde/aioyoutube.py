# **aioyoutube**.**py**
An asynchronous python API wrapper for the YouTube Data API. **Note, this repository and package is now archived. There are no guarantees the code and information is up to date.**

## Features
* Full coverage of all functionality in the YouTube Data API [reference guide](https://developers.google.com/youtube/v3/docs).
* Naming convention that matches official documentation.
* Option to enable debugging feature.
* Utilizes `async` and `await` python syntax.

## Installing
`pip install aioyoutube.py`

## Setup 
1. Access the Google API console with a google account.
2. Create a project in the  Google API console.
3. Enable project access to the YouTube Data API.
4. Create your credentials and generate an API key.
5. If applicable, register and generate OAuth 2.0 credentials.

## Basic Example

```
import os
import sys
import asyncio
from aioyoutube import YouTubeClient
from dotenv import load_dotenv

# load secret
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# returns links to the terms entered as arguments to the program
# ex search.py surfing violin
async def search(terms: list):

    client = YouTubeClient.from_connect(key=YOUTUBE_API_KEY)

    tasks = []
    for term in terms:
        tasks.append(client.search(search=term))
    
    results = await asyncio.gather(*tasks)
    for result in results:
        for item in result.json['items']:
            print('https://www.youtube.com/watch?v=' + item['id']['videoId'])
    await client.close()

if __name__ == '__main__':    

    loop = asyncio.get_event_loop()
    loop.run_until_complete(search(sys.argv[1:]))
```

## Requirements
This library requires the `aiohttp` library which is distrubuted under the Apache 2.0 license.

## License
`aioyoutube.py` is offered under the MIT License.

## Links
* [YouTube Data API](https://developers.google.com/youtube/v3)
* [Examples](https://github.com/im-mde/aioyoutube.py/tree/master/examples)
* [Setup Instructions](https://developers.google.com/youtube/registering_an_application)
* [aiohttp Repository](https://github.com/aio-libs/aiohttp)

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
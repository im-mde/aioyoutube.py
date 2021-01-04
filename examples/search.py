import asyncio
import os
from aioyoutube import YouTubeAPIClient
from dotenv import load_dotenv

# load secret
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# outputs json result of a search to the YouTubeAPIClient
async def search_youtube(client: YouTubeAPIClient, search_term: str, **kwargs):
    print(await client.search(search_term=search_term, **kwargs))
    print('\nYouTube search complete for {}\n'.format(search_term))

# concurrently makes a search request for different search terms
async def search(loop, search_terms: list):
    client = YouTubeAPIClient(key=YOUTUBE_API_KEY)
    tasks = []
    
    for search_term in search_terms:
        tasks.append(loop.create_task(search_youtube(client=client, search_term=search_term)))

    await asyncio.gather(*tasks, loop=loop)
    await client.close_session()

if __name__ == '__main__':
    amount = 0
    while amount > 5 or amount <= 0:
        amount = int(input('\nEnter amount of YouTube searches you want [1-5]: '))

    search_terms = []
    for i in range(amount):
        search_terms.append(input('Search {}: '.format(i + 1)))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(search(loop, search_terms))
    loop.close()
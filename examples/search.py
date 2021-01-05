import asyncio
import os
from aioyoutube import YouTubeAPIClient
from dotenv import load_dotenv

# load secret
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# concurrently running tasks searching different search terms from user input
async def search(loop, search_terms: list):
    client = await YouTubeAPIClient.from_connect(YOUTUBE_API_KEY)

    tasks = []
    for search_term in search_terms:
        tasks.append(loop.create_task(client.search(search_term=search_term)))

    await asyncio.gather(*tasks, loop=loop)

    for i, task in enumerate(tasks):
        print('\nResults for "{}":\n'.format(search_terms[i]))
        for video in task.result()['items']:
            print('\t{}'.format(video['snippet']['title']))
    print('\nYouTube Results Completed.\n')
    
    await client.close_session()

if __name__ == '__main__':
    print('\nExecuting Youtube Search Program.\n')

    # search amount limited to avoid reaching api quota
    amount = 0    
    while amount > 5 or amount <= 0:
        amount = int(input('Enter amount of YouTube searches you want [1-5]: '))

    search_terms = []
    for i in range(amount):
        search_terms.append(input('\nSearch {}: '.format(i + 1)))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(search(loop, search_terms))
    loop.close()
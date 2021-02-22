import os
from discord.ext import commands
from aioyoutube import YouTubeClient
from dotenv import load_dotenv

"""
    load secrets into memory from .env 
    
    NOTE: 
    you can have your youtube key and and discord token in your source code
    as strings but it is bad practice
"""

load_dotenv()
YOUTUBE_KEY = os.getenv('YOUTUBE_API_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


description = 'Basic discord bot using search coroutine from aioyoutube library'
bot = commands.Bot(command_prefix='?', description=description)

youtube = YouTubeClient.from_connect(key=YOUTUBE_KEY)


# searches for a keyword or keywords entered as an argument to the search command
# and lists out the first 5 relevant youtube links in the discord channel

@bot.command()
async def search(ctx, search):
    
    try:
        result = await youtube.search(search=str(search), maxResults='5')

        youtube_links = []
        for item in result.json['items']:
            youtube_links.append('https://www.youtube.com/watch?v=' + item['id']['videoId'])
        
        await ctx.send('\n'.join(youtube_links))
    except:
        await ctx.send('Something went wrong searching for "{}".'.format(search))


# cleanly shuts down this discord bot instance

@bot.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await youtube.close()
    await bot.close()

bot.run(DISCORD_TOKEN)
import discord
from discord.ext import tasks

from bs4 import BeautifulSoup
import urllib.request as urllib
import urllib.error as urllibErr
import time
import sys
import random

url_list = [
    "https://domain.com/reduktornyye/",
    "https://domain.com/tsilindrovyye/",
    "https://domain.com/aviatsionnyye/"
    ]


def goGetData(url):
    opener = urllib.build_opener()
    opener.addheaders = [('User-Agent', 'Robot LUM SEO monitoring')]
    #html_doc = opener.open(url)
    
    try:
        html_doc = opener.open(url)
    except urllibErr.HTTPError as e:
        if e.code == 404:
            return ['404', '404', '404']
    soup = BeautifulSoup(html_doc)
    #print(get_title(soup))
    #print(get_h1(soup))
    #print(get_description(soup))
    #cols = soup.findAll(['title', 'h1', 'meta'])
    #result = soup.title.text
    #result = result.decode('utf8')
    return [get_title(soup) , get_h1(soup), get_description(soup)]


def get_title(html):
    """Scrape page title"""
    title = None
    if html.title.string:
        title = html.title.string
    else:
        title = "TITLE NOT FOUND!"
    return title


def get_h1(html):
    """Scrape H1"""
    h1 = None
    h1 = html.find("h1")
    if h1:
        h1 = h1.string
    else:
        h1 = "H1 NOT FOUND!"
    return h1


def get_description(html):
    """Scrape page description"""
    description = None
    description = html.find("meta", attrs={'name': 'description'})
    if description:
        description = description.get('content')
    else:
        description = "META DESCRIPTION NOT FOUND!"
    return description







class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Robot LUM SEO monitoring. За работу...')
        print('------')
        channel = self.get_channel(11111111111111111111111)  # channel ID goes here
        await channel.send('Robot LUM SEO monitoring. За работу...')
        await self.my_background_task.start()


    @tasks.loop(minutes=15)  # task runs every 60 seconds
    async def my_background_task(self):
        res_msg = ""
        for url in url_list:
            res = goGetData(url)
            res_msg += "<" + url + "> : " + res[0] + "\n"
            # Если 404, то отправим инфу в канал 694526406280872017
            if res[0] == "404":
                channel = self.get_channel(11111111111111111111111)  # channel ID goes here
                await channel.send("ВНИМАНИЕ! Сломалась посадка: <" + url + ">")
            # Тут вздремнем чуть, чтобы не раздражать сервер
            time.sleep(random.randint(2,5))

        #channel = self.get_channel(11111111111111111111111)  # channel ID goes here
        #await channel.send(res_msg)

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient(intents=discord.Intents.default())
client.run('DISCORD TOKEN')


print("FINISH")
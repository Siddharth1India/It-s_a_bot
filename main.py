import discord
import os
import requests
import json
from dotenv import load_dotenv
import arxiv


def help():
    help_str = """Here are commands for bot:\n\n    $repo: Use this command to get top repos for any search query\n    $paper: Use this command to get top papers for any search query\n\nHappy Learning!"""
    return help_str


def github(keyword):
    repo_url = f"https://api.github.com/search/repositories?q={keyword}"
    repo_response = requests.get(repo_url)

    output = {}
    if repo_response.status_code == 200:
        repo_data = repo_response.json()

        for item in repo_data["items"][:5]:
            output[item['name']] = item['html_url']

        output_str = f'Here are top repositories for {keyword} :smile:\n\n'
        counter = 0
        for key, value in output.items():
            counter += 1
            output_str += f"{counter}. {key}\n <{value}>\n"
        output_str += "\nHappy Learning! :partying_face:"
        return output_str

    else:
        return "Failed to retrieve data"


def paper(keyword):
    paper_response = arxiv.Search(
        query=keyword,
        max_results=5,
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending
    )
    output = {}
    try:
        for result in paper_response.results():
            output[result.title] = result.pdf_url

        output_str = f'Here are top papers for {keyword} :smile:\n\n'
        counter = 0
        for key, value in output.items():
            counter += 1
            output_str += f"{counter}. {key}\n <{value}>\n"
        output_str += "\nHappy Learning! :partying_face:"
        return output_str
    except:
        return 'Failed to retrieve data'


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

my_secret = os.getenv('TOKEN')
print(my_secret)


@ client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@ client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$repo'):
        keyword = message.content
        keyword = keyword.lstrip('$repo ')
        repository = github(keyword)
        await message.channel.send(repository)

    if message.content.startswith('$paper'):
        keyword = message.content
        keyword = keyword.lstrip('$paper ')
        data_paper = paper(keyword)
        await message.channel.send(data_paper)

    if message.content.startswith('$help_ml_bot'):
        data_help = help()
        await message.channel.send(data_help)

client.run(my_secret)

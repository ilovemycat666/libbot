from books2 import search, cook, search2, bookdetails
import os
import random
import discord

print("loaded")
TOKEN = 'enter token here'
GUILD = 'enter guild here'

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

prefix = 'book:'
choose = ('!1', '!2', '!3', '!4', '!5')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global books
    if prefix in message.content.lower():
        query = message.content
        index = query.find("book:")
        index = index + 6
        response = search(query)
        # print(books)
        books = cook(response)
        # print(books[1]['link'])
        if len(books) == 0:
            await message.channel.send("No Results, Try Again")
        else:
            await message.channel.send("\n--Enter '!#' to choose your text\n")
            list_of_books = '\n\n'.join(
            book['title'] + book['author'] for book in books)
            await message.channel.send(list_of_books)
    elif message.content.lower().startswith(choose):
        choice = int(message.content[1:]) - 1
        soup = search2(books[choice]['link'])
        v = bookdetails(books[choice]['link'], soup)
        k = ['Title:\t',
             'Publish Date:\t',
             'Author:\t',
             'Description:\n', '']
        details = dict(zip(k, v))
        #await message.channel.send("Want to support bookbot? Buy him a virtual coffee at:\n(https://www.buymeacoffee.com/ilovemycat666)\n\n")
        #await message.channel.send("\n".join("{}{}".format(k, v)
                                    #for k, v in details.items()))

client.run(TOKEN)

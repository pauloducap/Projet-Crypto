import os
import discord
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print("le bot est prêt.")

@client.event
async def on_message(message):
    if message.content.lower() == "test":
        await message.channel.send("noob", delete_after=10)
    if message.content.startswith("!delete"):
        nbr = int(message.content.split()[1])
        messageList = await message.channel.history(limit=nbr+1).flatten()
        
        for delMessage in messageList:
            await delMessage.delete()
    
client.run(os.getenv("TOKEN"))

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as {0}!'.format(self.user))

#     async def on_message(self, message):
#         print('Message from {0.author}: {0.content}'.format(message))
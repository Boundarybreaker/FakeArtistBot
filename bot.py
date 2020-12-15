import discord
from discord import Message
import random

opted_in = []


class FakeArtBot(discord.Client):

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        if message.content.startswith('!fab optin'):
            opted_in.append(message.author)
            await message.channel.send('Opted in to Fake Artist Bot!')
        if message.content.startswith('!fab optout'):
            opted_in.remove(message.author)
            await message.channel.send('Opted out of Fake Artist Bot!')
        if message.content.startswith('!fab round '):
            prompt = message.content[len('!fab round '):]
            fake = random.choice(opted_in)
            while fake == message.author:
                fake = random.choice(opted_in)
            for author in opted_in:
                if author != fake and author != message.author:
                    dm = author.dm_channel
                    if dm is None:
                        await author.create_dm()
                        dm = author.dm_channel
                    await dm.send('You are an artist! Your prompt is: ' + prompt)
            dm = fake.dm_channel
            if dm is None:
                await fake.create_dm()
                dm = fake.dm_channel
            await dm.send('You are the FAKE this round!')
            await message.channel.send('The prompt has been sent out!')


client = FakeArtBot()
client.run(open('tokensecret.txt').read())

import discord
import matplotlib.pyplot as plt
import os
import seaborn as sns
from collections import OrderedDict

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!graph'):
        await message.channel.send('Calculating...')

        textChannels = []
        for channel in message.guild.text_channels:
            textChannels.append(channel)

        print(textChannels)
        userCountDict = {}
        for textChannel in textChannels:
            async for msg in textChannel.history(limit=None):
                if msg.author != client.user:
                    key = msg.author.name + '#' + msg.author.discriminator
                    userCountDict[key] = userCountDict.get(key, 0) + 1

        orderedDict = OrderedDict(sorted(userCountDict.items(), key=lambda x: x[1]))

        labels = list(orderedDict.keys())
        values = list(orderedDict.values())

        explode = [0] * len(labels)
        for i, val in enumerate(values):
            total = sum(values)
            fracture = val/total
            explode[i] = max(0, 1 - (fracture * 7));

        colors = sns.color_palette(sns.palplot(sns.husl_palette(len(labels), s=.4)))

        fig1, ax1 = plt.subplots()
        wedges, texts, autotexts = ax1.pie(
            values, explode=explode, labels=labels, colors=colors, autopct=make_autopct(values), shadow=True, startangle=140)
        ax1.axis('equal')
        ax1.set_title("User posts made")
        fig1.savefig('fig.png', dps=100)

        await message.channel.send(file=discord.File('fig.png'))

        if os.path.exists("fig.png"):
            os.remove('fig.png')


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%\n({v:d})'.format(p=pct, v=val)
    return my_autopct


sns.set_context("paper")
client.run('NzEzMDE0NDM5MDQ0OTcyNTY1.XsZ_Fw.1dkV_X3GjoBSB6ld6c_rBB0DtAc')

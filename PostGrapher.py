import discord
import matplotlib.pyplot as plt
import os
import seaborn as sns
import numpy as np
import random as r
from collections import Counter, OrderedDict
import itertools

client = discord.Client()
figsize = (10,10)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    splitMsg = message.content.split()
    if splitMsg[0] == '!graph' and (splitMsg[1] == 'bar' or splitMsg[1] == 'pie'):
        await message.channel.send('Valid arguments! Calculating...')

        textChannels = []
        for channel in message.guild.text_channels:
            textChannels.append(channel)

        userCountDict = {}
        for textChannel in textChannels:
            async for msg in textChannel.history(limit=None):
                if msg.author != client.user:
                    key = msg.author.name + '#' + msg.author.discriminator
                    userCountDict[key] = userCountDict.get(key, 0) + 1

        cntSize = len(userCountDict)
        if (len(splitMsg) > 2 and splitMsg[2].isdigit()):
            cntSize = max(1, int(splitMsg[2]))

        cnt = dict(Counter(userCountDict).most_common(cntSize))

        labels = list(cnt.keys())
        values = list(cnt.values())
        colors = sns.color_palette(sns.palplot(sns.husl_palette(len(labels), s=.4)))

        if splitMsg[1] == 'bar':
            make_bar_chart(labels, values, colors)
        elif splitMsg[1] == 'pie':
            make_pie_chart(labels, values, colors)
        else:
            await message.channel.send('Unknown argument. Stopping.')
 
        if os.path.exists("fig.png"):
            await message.channel.send(file=discord.File('fig.png'))
            os.remove('fig.png')

def make_bar_chart(labels, values, colors):
    x = np.arange(len(labels))
    width = 0.1
    fig, ax = plt.subplots(figsize=figsize)
    rects = ax.bar(x, values, width, color=colors[r.randint(0, len(colors) - 1)], edgecolor=colors[r.randint(0, len(colors) - 1)])
    ax.set_ylabel('Number of posts')
    ax.set_title('User posts made')
    ax.set_xticks(x)
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    ax.set_xticklabels(labels)
    autolabel(rects, ax, values)

    fig.tight_layout()
    fig.savefig('fig.png', dpi=100)

def autolabel(rects, ax, values):
    for rect in rects:
        height = rect.get_height()
        annotateText = get_percentage_and_total(values, height)
        ax.annotate(annotateText,
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 1),
                    textcoords="offset points",
                    ha='center')

def make_pie_chart(labels, values, colors):
    explode = [0] * len(labels)
    for i, val in enumerate(values):
        total = sum(values)
        fracture = val/total
        explode[i] = max(0, 1 - (fracture * 7));

        fig1, ax1 = plt.subplots(figsize=figsize)
        wedges, texts, autotexts = ax1.pie(
            values, explode=explode, labels=labels, colors=colors, autopct=make_autopct(values), shadow=True, startangle=140)
        ax1.axis('equal')
        ax1.set_title("User posts made")
        fig1.savefig('fig.png', dpi=100)

def get_percentage_and_total(values, height):
    total = sum(values)
    percentage = float(height/total) * 100
    return '{p:.2f}%\n({v:d})'.format(p=percentage, v=height)


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%\n({v:d})'.format(p=pct, v=val)
    return my_autopct

with open ('conf', 'r') as config:
    data=config.read()

sns.set_context("paper")
client.run(data)
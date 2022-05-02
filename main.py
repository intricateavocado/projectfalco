#!/usr/bin/env python

#libraries
import os
import random #for quickfacts and dailyfacts randomization
import discord #discord api access
import asyncpg
from discord.ext import tasks, commands
from datetime import date #storing date and time for facthistory


dailyfactpick = 'N/A' #default daily fact on startup
whatfactcheck = False
alreadyscheduled = False
boolscheduled = False
quickfactsused = []
templist = []
alreadyscheduled = False
whatfact = ''
facthistory = []
scheduledfacts = []
a_file = open("factlist.txt", "r")

lines = a_file.read()
facts = lines.splitlines()

a_file.close()

TOKEN = 'DISCORD_TOKEN'
GUILD = 'DISCORD_GUILD'

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    fact.start()

@tasks.loop(hours=24)
async def fact():
    global channel
    global dailyfactpick
    global facthistory
    global boolscheduled
    today = str(date.today())
    for x in range(len(scheduledfacts)):
        if scheduledfacts[x]['date'] == today:
            print('Fact already set.')
            dailyfactpick = scheduledfacts[x]['fact']
            facthistory.append({'date':today, 'fact':dailyfactpick}) #add it to the history
            print('Fact located.')
            boolscheduled = True
    if boolscheduled == False:
        dailyfactpick = random.choice(facts) #pick a daily fact
        facthistory.append({'date':today, 'fact':dailyfactpick}) #add it to the history
        facts.remove(dailyfactpick) #remove the fact from selection
        textfile = open("factlist.txt", "w")
        for element in facts:
            textfile.write(element + "\n")
        textfile.close()
    channel = bot.get_channel(958103723631067187)
    embed=discord.Embed(title="Daily Fact", description=dailyfactpick, color=discord.Color.purple())
    await channel.send(embed=embed)

@bot.command()
async def setfact(ctx, arg):
    global dailyfactpick
    global facthistory
    global alreadyscheduled
    dateinput = arg
    for x in range(len(scheduledfacts)):
        if scheduledfacts[x]['date'] == dateinput:
            alreadyscheduled = True
            datescheduled = x
        else:
            alreadyscheduled = False
    if alreadyscheduled == True:
        embed=discord.Embed(title="That date is already scheduled.", color=discord.Color.purple())
        embed.add_field(name='The fact for ' + dateinput + ' is:', value=scheduledfacts[datescheduled]['fact'])
        embed.add_field(name='Would you like to change it? (Y/N)')
        await channel.send(embed=embed)
        msg = await bot.wait_for("message")
        tempmsg = msg.content
        tempmsg = tempmsg.capitalize()
        if tempmsg == 'Y':
            embed=discord.Embed(title="Enter fact below:", color=discord.Color.purple())
            await channel.send(embed=embed)
            msg = await bot.wait_for("message")
            addfactpend = msg.content
            scheduledfacts.append({'date':dateinput, 'fact':addfactpend}) #add it to the future
            embed=discord.Embed(title="Fact added!", description=addfactpend, color=discord.Color.purple())
            await channel.send(embed=embed)
        else:
            embed=discord.Embed(title="Fact cancelled.", color=discord.Color.purple())
            await channel.send(embed=embed)
    else:
        embed=discord.Embed(title="Enter fact to add below: ", color=discord.Color.purple())
        await channel.send(embed=embed)
        msg = await bot.wait_for("message")
        tempmsg = msg.content
        scheduledfacts.append({'date':dateinput, 'fact':tempmsg}) #add it to the future
        embed=discord.Embed(title="Fact added!", color=discord.Color.purple())
        embed.add_field(name='The fact for ' + dateinput + ' is now:', value=tempmsg)
        await channel.send(embed=embed)

@bot.command()
async def upcoming(ctx):
    embed=discord.Embed(title="Upcoming Facts", color=discord.Color.purple())
    rangex = len(scheduledfacts)
    if rangex > 9:
        rangex = 9
    for x in range(rangex):
        embed.add_field(name=scheduledfacts[x]['date'], value=scheduledfacts[x]['fact'])
    await channel.send(embed=embed)

@bot.command()
async def quickfact(ctx):
    global quickfactsused
    global dailyfactpick
    global templist
    for element in facts:
        if element in quickfactsused:
            print("Skipping...")
        elif element == dailyfactpick:
            print("Skipping...")
        else:
            templist.append(element)
        if templist == []:
            quickfactsused = []
            for element in facts:
                if element in quickfactsused:
                    print("Skipping...")
                elif element == dailyfactpick:
                    print("Skipping...")
                else:
                    templist.append(element)
    response = random.choice(templist)
    quickfactsused.append(response)
    embed=discord.Embed(title="Quick Fact", description=response, color=discord.Color.purple())
    await channel.send(embed=embed)

@bot.command()
async def whatfact(ctx, arg):
    global whatfactcheck
    global facthistory
    global whatfact
    dateinput = arg
    for x in range(len(facthistory)):
        if facthistory[x]['date'] == dateinput:
            whatfact = facthistory[x]['fact']
            whatfactcheck = True
    if whatfactcheck == False:
        whatfact = 'No fact found on ' + dateinput
    embed=discord.Embed(title=dateinput, description=whatfact, color=discord.Color.purple())
    await channel.send(embed=embed)
    whatfactcheck = False

@bot.command()
async def about(ctx):
    embed=discord.Embed(title="About Me", description='made by @uncenter#1078  |  ayo.so/uncenter', color=discord.Color.purple())
    await channel.send(embed=embed)

@bot.command()
async def dailyfact(ctx):
    global dailyfactpick
    global whatfactcheck
    response = dailyfactpick
    embed=discord.Embed(title="Daily Fact", description=response, color=discord.Color.purple())
    await channel.send(embed=embed)

@bot.command()
async def addfact(ctx, *args):
    global dailyfactpick
    global whatfactcheck
    global templist
    global facthistory
    print(args)
    if len(args) < 5:
        embed=discord.Embed(title="Enter your fact below: ", color=discord.Color.purple())
        await channel.send(embed=embed)
        msg = await bot.wait_for("message")
        addfactpend = msg.content
    else: 
        addfactpend = args
    if addfactpend in facts:
        embed=discord.Embed(title="This fact is already in the list. Action cancelled.", color=discord.Color.purple())
        await channel.send(embed=embed)
    elif addfectpend in facthistory:
        embed=discord.Embed(title="This fact is already in the list. Action cancelled.", color=discord.Color.purple())
        await channel.send(embed=embed)
    else:
        embed=discord.Embed(title="Is this correct? (Y/N)", color=discord.Color.purple())
        embed.add_field(name="Pending Fact: ", value=addfactpend)
        await channel.send(embed=embed)
        msg = await bot.wait_for("message")
        tempmsg = msg.content
        tempmsg = tempmsg.capitalize()
        if tempmsg == 'Y':
            facts.append(addfactpend)
            textfile = open("factlist.txt", "w")
            for element in facts:
                textfile.write(element + "\n")
            textfile.close()
            embed=discord.Embed(title="Fact added!", description=addfactpend, color=discord.Color.purple())
            await channel.send(embed=embed)
        else:
            embed=discord.Embed(title="Fact cancelled.", color=discord.Color.purple())
            await channel.send(embed=embed)

@bot.command(aliases=['removefacts', 'delete', 'remove'])
async def removefact(ctx, *args):
    global quickfactsused
    global dailyfactpick
    global whatfactcheck
    global templist
    global facthistory
    if args == '':
        embed=discord.Embed(title="Enter the fact to remove below: ", color=discord.Color.purple())
        await channel.send(embed=embed)
        msg = await bot.wait_for("message")
        removefactpend = msg.content
    else:
        removefactpend = args
    embed=discord.Embed(title="Is this correct? (Y/N)", color=discord.Color.purple())
    embed.add_field(name="Pending Fact Removal:", value=removefactpend)
    await channel.send(embed=embed)
    msg = await bot.wait_for("message")
    if msg.content == 'Y':
        facts.remove(removefactpend)
        textfile = open("factlist.txt", "w")
        for element in facts:
            textfile.write(element + "\n")
        textfile.close()
        embed=discord.Embed(title="Fact removed!", description=removefactpend, color=discord.Color.purple())
        await channel.send(embed=embed)
    else:
        embed=discord.Embed(title="Fact remove cancelled.", color=discord.Color.purple())
        await channel.send(embed=embed)

@bot.command()
async def listfacts(ctx):
    await channel.send(file=discord.File("factlist.txt"))

@bot.command()
async def commands(ctx):
    embed=discord.Embed(title="Help", description="Welcome to RandomFactBot! Here are my commands:", color=discord.Color.purple())
    embed.set_author(name="uncenter", url="https://ayo.so/uncenter", icon_url="https://cdn.ayo.so/117149d5c4a0e3db788313a45b71187c62db08655adeaf1e.webp")
    embed.add_field(name="$quickfact", value="sends a random fact from the catalog (changes every time)", inline=False)
    embed.add_field(name="$dailyfact", value="sends the fact of the day", inline=False)
    embed.add_field(name="$whatfact", value="what fact was on <date> (ex. $whatfact 2022-04-20)", inline=False)
    embed.add_field(name="$addfact", value="adds a fact to the catalog", inline=False)
    embed.add_field(name="$removefact", value="removes a fact from the catalog", inline=False)
    embed.add_field(name="$listfacts", value="sends the fact catalog as a text file", inline=False)
    embed.add_field(name="$about", value="all about me!", inline=False)
    embed.add_field(name="$commands", value="sends this! :)", inline=False)
    await channel.send(embed=embed)
    # await channel.send(file=discord.File("help.txt"))
    

bot.run(TOKEN)

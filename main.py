import discord
import os
from replit import db
from keep_alive import keep_alive
from bs4 import BeautifulSoup
from requests import get

client = discord.Client()

TOKEN = os.environ['TOKEN']

levisURL = 'https://eune.op.gg/summoner/userName=Lev%C3%ADs'
estebanURL1 = 'https://eune.op.gg/summoner/userName=mid+diff+sorry'
estebanURL2 = 'https://eune.op.gg/summoner/userName=XXDXDDXDD'

def update_links(link_message):
  if "links" in db.keys():
    links = db["links"]
    links.append(link_message)
    db["links"] = links
  else:
    db["links"] = [link_message]

def delete_link(index):
  links = db["links"]
  if len(links) > index:
    del links[index]
    db["links"] = links

def getSummonerInfo(bSoup):
  soloq = bSoup.find('div', class_ = 'TierRankInfo')
  name = bSoup.find('span', class_ = 'Name').get_text()
  queueType = soloq.find('div', class_ = 'RankType').get_text()
  soloqRank = soloq.find('div', class_ = 'TierRank').get_text()
  lp = soloq.find('span', class_ = 'LeaguePoints').get_text().strip()
  winRatio = soloq.find('span', class_ = 'winratio').get_text()
  mess = ("==========================\r\n" + 
  "__**Summoner Name:**__ `" + name + "`\r\n" +
  "__**Queue Type:**__ `" + queueType + "`\r\n" +
  "__**Rank:**__ `" + soloqRank +  "`\r\n" +
  "__**LP:**__ `" + lp  + "`\r\n" +
  "__**WR:**__ `" + winRatio + "`\r\n" + 
  "==========================")
  return mess

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("$help"):
    helpMsg = "Use these commands to use this bot:\n`$add <link>` - adds a new link to the database\n`$del <index>` - deletes a link from the database\n`$delall` - deletes all links from the database\n`$links` - shows saved handy links\n`$stats <name>` - displays the most important info about LoL Summoner from OP.GG"
    await message.channel.send(helpMsg)

  if msg.startswith("$add "):
    link_message = msg.split("$add ",1)[1]
    if(len(link_message) < 200):
      update_links(link_message)
      await message.channel.send("New link added!")
    else:
      await message.channel.send("Link too long!")


  if msg.startswith("$del "):
    links = []
    if "links" in db.keys():
      index = int(msg.split("$del ",1)[1])
      if index > 0 and index <= len(db["links"]):
        delete_link(index-1)
        links = db["links"]
        await message.channel.send("Link successfully deleted!")
      else:
        await message.channel.send("No such index to delete!")
  
  if msg.startswith("$replace "):
    await message.channel.send("Functionality not yet implemented!")

  if msg.startswith("$delall"):
      for i in range(len(db["links"])):
        delete_link(0)
      await message.channel.send("You've deleted all links!")

  if msg.startswith("$links"):
    links = []
    itr = 1
    mess = ""
    if len(db["links"]) > 0:
      links = db["links"]
      for link in links:
        mess += str(itr) + ". " + link + "\n"
        itr += 1
    else:
      mess = "No links!\nAdd some using `$add` command."
    await message.channel.send(mess)

  if msg.startswith("$stats "):
    climb_target = msg.split("$stats ",1)[1]
    if(climb_target.lower() == 'levis' or climb_target.lower() == 'levi' or climb_target.lower() == 'sou'):
      page = get(levisURL)
      bSoup = BeautifulSoup(page.content, 'html.parser')
      mess = getSummonerInfo(bSoup)
      await message.channel.send(mess)
      
    elif(climb_target.lower() == 'esteban' or climb_target.lower() == 'ban' or climb_target.lower() == 'banek'):
      page = get(estebanURL1)
      bSoup = BeautifulSoup(page.content, 'html.parser')
      mess = getSummonerInfo(bSoup)
      page = get(estebanURL2)
      bSoup = BeautifulSoup(page.content, 'html.parser')
      mess = mess[0:len(mess)-27] + "\n" + getSummonerInfo(bSoup)
      await message.channel.send(mess)

keep_alive()
client.run(TOKEN)

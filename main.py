import discord
import os
import json
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

def isSou(name):
  if name == 'levis' or \
  name == 'levi' or \
  name == 'sou' or \
  name == 'igor' or \
  name == 'challenger' or \
  name == 'zuczek':
    return True
  return False

def isEsteban(name):
  if name == 'esteban' or \
  name == 'ban' or \
  name == 'banek' or \
  name == 'este' or \
  name == 'rozek' or \
  name == 'daniel':
    return True
  return False


def getSummonerInfo(bSoup):
  soloq = bSoup.find('div', class_ = 'TierRankInfo')
  name = bSoup.find('span', class_ = 'Name').get_text()
  queueType = soloq.find('div', class_ = 'RankType').get_text()
  soloqRank = soloq.find('div', class_ = 'TierRank').get_text()
  lp = soloq.find('span', class_ = 'LeaguePoints').get_text().strip()
  winRatio = soloq.find('span', class_ = 'winratio').get_text()
  mess = ("==========================\n" + 
  "**• Summoner Name:** `" + name + "`\n" +
  "**• Queue Type:** `" + queueType + "`\n" +
  "**• Rank:** `" + soloqRank +  "`\n" +
  "**• LP:** `" + lp  + "`\n" +
  "**• WR:** `" + winRatio + "`\n" + 
  "==========================")
  return mess

def getSummonerHistory(bSoup):
  gameAmount = 0
  mess = ""
  name = bSoup.find('span', class_ = 'Name').get_text()
  for game in bSoup.find_all('div', class_ = 'GameItemWrap'):
    if(gameAmount < 5):
      gameType = game.find('div', class_ = 'GameType').get_text().strip()
      gameResult = game.find('div', class_ = 'GameResult').get_text().strip()
      gameLength = game.find('div', class_ = 'GameLength').get_text().strip()
      championName = game.find('div', class_ = 'ChampionName').get_text().strip()
      KDAKills = game.find('span', class_ = 'Kill').get_text().strip()
      KDADeaths = game.find('span', class_ = 'Death').get_text().strip()
      KDAAssists = game.find('span', class_ = 'Assist').get_text().strip()
      KDARatio = game.find('div', class_ = 'KDARatio').get_text().strip()
      CS = game.find('div', class_ = 'CS').get_text().strip()
      mess = mess + ("==================================\n" +
      "GAME NUMBER: " + str(gameAmount+1) + ' ====================\n' +
      "**✍️ Sumonner name:** `----- " + name + "`\n" +
      "**👾 Game type:** `---------- " + gameType + "`\n" +
      "**🦸🏼‍♂️ Champion name:** `----- " + championName + "`\n" +
      "**🗡️ KDA:** `--------------- " + KDAKills + '/' + KDADeaths + '/' + KDAAssists + " = " + KDARatio + "`\n" +
      "**🤷 Game result:** `-------- " + gameResult +  "`\n" +
      "**👻 CS:** `----------------- " + CS + "`\n" +
      "**⏱️ Game length:** `-------- " + gameLength  + "`\n")
      gameAmount = gameAmount + 1
    else:
      break
  mess = mess + "==================================\n"
  return mess

def getJoke():
  response = get("https://official-joke-api.appspot.com/random_joke")
  jsonData = json.loads(response.text)
  joke = jsonData['setup']
  punchline = jsonData['punchline']
  return joke + '\n.\n.\n.\n' + punchline

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("$help"):
    helpMsg = "Use these commands to use this bot:\n• `$add <link>` - adds a new link to the database\n• `$del <index>` - deletes a link from the database\n• `$delall` - deletes all links from the database\n• `$links` - shows saved handy links\n• `$stats <name>` - displays the most important info about LoL Summoner from OP.GG\n• `$history <name>` - displays last 5 games from LoL Summoner's match history\n• `$joke` - sends a random joke to cheer up your day"
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
    stats_target = msg.split("$stats ",1)[1]
    if(isSou(stats_target.lower())):
      page = get(levisURL)
      bSoup = BeautifulSoup(page.content, 'html.parser')
      mess = getSummonerInfo(bSoup)
      await message.channel.send(mess)
    elif(isEsteban(stats_target.lower())):
      page = get(estebanURL1)
      bSoup = BeautifulSoup(page.content, 'html.parser')
      mess = getSummonerInfo(bSoup)
      page = get(estebanURL2)
      bSoup = BeautifulSoup(page.content, 'html.parser')
      mess = mess[0:len(mess)-27] + "\n" + getSummonerInfo(bSoup)
      await message.channel.send(mess)

  if msg.startswith("$history "):
    stats_target = msg.split("$history ",1)[1]
    if(isSou(stats_target.lower())):
      page = get(levisURL)
      bSoup = BeautifulSoup(page.content, 'html.parser')
      mess = getSummonerHistory(bSoup)
      await message.channel.send(mess)
    elif(isEsteban(stats_target.lower())):
      page = get(estebanURL1)
      bSoup = BeautifulSoup(page.content, 'html.parser')
      mess = getSummonerHistory(bSoup)
      await message.channel.send(mess)

  if msg.startswith("$joke"):
    page = get('https://official-joke-api.appspot.com/random_joke')
    bSoup = BeautifulSoup(page.content, 'html.parser')
    mess = getJoke()
    await message.channel.send(mess)
    

keep_alive()
client.run(TOKEN)

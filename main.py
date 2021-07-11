import discord
import os
from replit import db
from keep_alive import keep_alive

client = discord.Client()

TOKEN = os.environ['TOKEN']

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
    del links[index-1]
    db["links"] = links

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("$help"):
    helpMsg = "Use these commands to use this bot:\n`$add` - adds a new link to the database\n`$del` - deletes a link from the database\n`$delall` - deletes all links from the database\n`$links` - shows saved handy links"
    await message.channel.send(helpMsg)

  if msg.startswith("$add "):
    link_message = msg.split("$add ",1)[1]
    update_links(link_message)
    await message.channel.send("New link added!")

  if msg.startswith("$del "):
    links = []
    if "links" in db.keys():
      index = int(msg.split("$del ",1)[1])
      if index > 0 and index <= len(db["links"]):
        delete_link(index)
        links = db["links"]
      else:
        await message.channel.send("No such index to delete!")
  
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

keep_alive()
client.run(TOKEN)

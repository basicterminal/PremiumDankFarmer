import discord, time, os
from discord.ext import commands

from replit import db
import random, requests

#                         #

class Sequence:
      _Author_Id = "Your ID Here"
      _Farming = False
      #                          #

class Data:
      Token = ""
      Sleep = 5
      #                          #

class Path:
      Tokens = "data/tokens.txt"
      Proxies = "data/proxies.txt"
      #                          #

class Database:
      Load = []

      db["Used"] = []
      db["Starter"] = []

      db["Ratelimited"] = []
      db["Proxies"] = []
      #                          #

class Dank:
      class Identifier:
            Max = 9
      class Amounts:
            Betting = "max"
            SnakeEye = "max"
      
      Growth_Commands = ["beg", "hunt", "fish", "dig"]
      Starter_Commands = ["newplayerpack", "meme", "bet", "se"]

      Keep_Items = ["bank", "meme", "normie", "daily", "pizza"]
      Sell_Items = ["boar", "fish", "skunk", "trash", "rarefish"]

#-----------------#

class guru:
      bot = ""
      def __init__(self, prefix: str, author_id: str):
          guru.bot = commands.Bot(
                self_bot = True,
                command_prefix = prefix
          )

    
          async def SendMessage(channel_id: str, message_content: str):
                channel = bot.get_channel(
                          channel_id
                )

                #----- READ ------#
                # This is for the current session of the bot, not any other tokens
                #-----------------#

                await channel.send(
                      message_content
                )

          def SendMessageAs(channel_id: str, message_content: str, token: str):
              try:
                  user = requests.get(
                      "https://discordapp.com/api/v9/users/@me",
                      headers = {
                                "Authorization": token
                      }
                  )

                  user_json = user.json()
                  user_email = user_json["email"]
                  user_identification = user_json["id"]
                  

                  if user.status_code == 200:
                     print (" [🟢] Logged into {} ({})".format(user_email, user_identification))
                     try:
                        r = requests.post(
                            "https://discordapp.com/api/v9/channels/{}/messages".format(
                                  channel_id
                            ), headers = {
                                    "Authorization": token
                            }, json = {
                                    "content": message_content
                            }
                        )

                        if r.status_code == 200:
                           print (" [🟢] Success! | ({})".format(channel_id))
                        else:
                           print (" [🔴] Failed | Message could not be sent")
                     except Exception as E:
                        print (E)
                  else:
                      print (" [🔴] Failed to Login")    
              except Exception as E:
                     print (E)
                 
                       
#--------#
bot = guru(prefix = "dank", author_id = Sequence._Author_Id)


@guru.bot.event
async def on_ready():
      print (" [👍] Ready as {} ({})\n#----------------------#".format(guru.bot.user.name, guru.bot.user.id))

@guru.bot.command(aliases=["load"])
async def queue(ctx):
      with open(Path.Tokens, "r") as tokens:
           Database.Load = []
           Database.Load += [token.strip() for token in tokens.readlines()]

      await ctx.send(
            embed = discord.Embed(
                    title = "Loaded Tokens",
                    description = "{} was successfully loaded into the database".format(len(Database.Load))
            )
      )

@guru.bot.command(aliases=["quit"])
async def stop(ctx):
      if Sequence._Farming == True:
         Sequence._Farming = False
         
         await ctx.send(
               embed = discord.Embed(
                       title = "Stopped Farming",
                       description = "Current farming session was ended"
               )
         )
      else:
        await ctx.send(
              embed = discord.Embed(
                      title = "Error",
                      description = "You weren't previously farming"
              )
        )

@guru.bot.command(aliases=["farm"])
async def start(ctx):
      if Sequence._Farming == False and len(Database.Load) > int(Dank.Identifier.Max):
         await ctx.send(
               embed = discord.Embed(
                       title = "Bot Started",
                       description = "Running with {} tokens".format(len(Database.Load))
               )
         )
         #                          #
         Sequence._Farming = True
         while Sequence._Farming == True:
               for Token in Database.Load:
                   if Token in set(db["Used"]):
                      for Command in Dank.Growth_Commands:
                          bot.SendMessageAs(ctx.channel.id, Command, Token)
                      time.sleep(int(Data.Sleep))
                   else:
                        for Command in Dank.Starter_Commands:
                            if Command == "newplayerpack" or "meme":
                               Parsed = "pls use {}".format(Command)
                            else:
                               Parsed = "pls {} {}".format(Command, Dank.Amounts.Betting)
                               
                            db["Used"] += [Token]
                            bot.SendMessageAs(ctx.channel.id, Parsed, Token)
     
      else:
           await ctx.send(
                 embed = discord.Embed(
                         title = "Error",
                         description = "Either the bot is already farming, or you dont have over 9 tokens.."
                 )
           )

@guru.bot.command(aliases=["recieve"])
async def get(ctx): 
      _Total = 0     
      _Success = 0
    
      for Token in Database.Load:
          try:
              bot.SendMessageAs(ctx.author.id, "", Token)
              print (" [🟢] Sent all coins to {} ({})".format(Sequence._Author_Id, Token))
              _Success += 1
              _Total += 1
          except:
              print (" [🔴] Could not send coins ({})".format(Token))
              _Total += 1
      
      await ctx.send(
            embed = discord.Embed(
                    title = "Output",
                    description = "(`{}`/`{}`) was the amount of bots that given money to you"
            )
      )

#_-------------_#
guru.bot.run(Data.Token, bot = False)
#_-------------_#

# I knew you would scroll to the bottom, but I want to inform you about the bot.
# This may not work as of me not knowing what I am doing right now since I have not been working on python for weeks.

# Please create an issue and tell me what happend / is happening

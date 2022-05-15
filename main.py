import os
import re
import sys
import traceback
import discord
from discord.ext import commands, tasks
bot = discord.Client()
@bot.event
async def on_ready():
    change_status.start()
    print(f"'{bot.user.name}' Online!")
    
@bot.event
async def on_message(message):
    if not message.guild or message.author.id == bot.user.id:
        return
      
    if (m := re.match(r"^<a?:[\w]+:([\d]+)>$", message.content)):
        if message.content.startswith("<a:"):
            ext = "gif"
        else:
            ext = "png"
            
        embed = discord.Embed(color=message.author.color)
        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar)
        embed.set_image(url=f"https://cdn.discordapp.com/emojis/{m.group(1)}.{ext}")
        
        await message.channel.send(embed=embed)
        await message.delete()
        
        
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        return
    else:
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        
        
@tasks.loop(minutes=5.0)
async def change_status():
    await bot.change_presence(activity=discord.Game(name=f"{len(bot.guilds)}개의 서버와 함께"))
    
    
bot.run("token")
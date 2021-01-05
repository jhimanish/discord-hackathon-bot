# bot.py
import os
import random
from dotenv import load_dotenv
import discord

# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 2
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="verify", pass_context=True)
async def verify(ctx, email_address):
    # reading files
    ieee_list_arr = []
    with open("ieeemembers.txt") as f:
        ieee_list_arr = f.read().splitlines()

    participants_arr = []
    with open("participants.txt") as f:
        participants_arr = f.read().splitlines()

    ieee_list_arr_used = []
    with open("ieeeused.txt") as f:
        ieee_list_arr_used = f.read().splitlines()

    participants_arr_used = []
    with open("participantsused.txt") as f:
        participants_arr_used = f.read().splitlines()

    # checking for ieee email address
    for i in ieee_list_arr:
        j = i.split()
        if j[0].lower() == email_address.lower():
            # moving to used list
            ieee_list_arr.remove(i)
            ieee_list_arr_used.append(i)
            await ctx.send("You have been verified", delete_after=3.0)
            # perms
            await ctx.author.edit(nick=j[-1] + " (" + " ".join(j[1:-1]) + ")")
            role = discord.utils.get(ctx.guild.roles, name="IEEE")
            await ctx.author.add_roles(role)
            role = discord.utils.get(ctx.guild.roles, name=" ".join(j[1:-1]))
            await ctx.author.add_roles(role)
            break

    # checking for participant email address
    for i in participants_arr:
        j = i.split()
        if j[0].lower() == email_address.lower():
            # moving to used list
            participants_arr.remove(i)
            participants_arr_used.append(i)
            await ctx.send("You have been verified", delete_after=3.0)
            # perms
            await ctx.author.edit(nick=" ".join(j[1:]))
            role = discord.utils.get(ctx.guild.roles, name="Hacker")
            await ctx.author.add_roles(role)
            break

    # writing to files
    with open("ieeemembers.txt", "w") as f:
        for item in ieee_list_arr:
            f.write("%s\n" % item)
    f.close()

    with open("participants.txt", "w") as f:
        for item in participants_arr:
            f.write("%s\n" % item)
    f.close()

    with open("ieeeused.txt", "w") as f:
        for item in ieee_list_arr_used:
            f.write("%s\n" % item)
    f.close()

    with open("participantsused.txt", "w") as f:
        for item in participants_arr_used:
            f.write("%s\n" % item)
    f.close()

    await ctx.message.delete(delay=2.0)


bot.run(TOKEN)
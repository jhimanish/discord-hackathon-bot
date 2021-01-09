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
# bot = commands.Bot(command_prefix="!")
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="info", pass_context=True)
@commands.has_any_role("MakeUofT Director", "MakeUofT Organizer", "IEEE")
async def info(ctx, *, name):
    # reading files
    participants_arr = []
    with open("participants.txt") as f:
        participants_arr = f.read().splitlines()

    # check if in participants list
    for i in participants_arr:
        j = i.split()
        if name.lower() in (" ".join(j[1:])).lower():
            await ctx.send(" ".join(j))


@bot.command(name="verify", pass_context=True)
async def verify(ctx, email_address):

    already_verified = False
    # check if user is already verified
    for role in ctx.author.roles:
        if "Hacker" == role.name or "IEEE" == role.name:
            already_verified = True
            await ctx.send(
                "You cannot use this command as you have already been verified.",
                delete_after=3.0,
            )
            break

    if already_verified == False:
        # reading files
        ieee_list_arr = []
        with open("ieeemembers.txt") as f:
            ieee_list_arr = f.read().splitlines()

        participants_arr = []
        with open("participants.txt") as f:
            participants_arr = f.read().splitlines()

        # checking for ieee email address
        for i in ieee_list_arr:
            j = i.split()
            if j[0].lower() == email_address.lower():
                # check if user already exists
                members = ctx.guild.members
                found = False
                for i in members:
                    if i.nick == (j[-1] + " (" + " ".join(j[1:-1]) + ")"):
                        for role in i.roles:
                            if "IEEE" == role.name:
                                found = True
                if found == False:
                    # send message about being verified
                    await ctx.send("You have been verified", delete_after=3.0)
                    # perms
                    await ctx.author.edit(nick=j[-1] + " (" + " ".join(j[1:-1]) + ")")
                    role = discord.utils.get(ctx.guild.roles, name="IEEE")
                    await ctx.author.add_roles(role)
                    role = discord.utils.get(ctx.guild.roles, name=" ".join(j[1:-1]))
                    await ctx.author.add_roles(role)
                if found == True:
                    await ctx.send(
                        "This email has already been used. If this is an error, please contact @Himanish",
                        delete_after=3.0,
                    )
                break

        # checking for participant email address
        for i in participants_arr:
            j = i.split()
            if j[0].lower() == email_address.lower():
                # check if user already exists
                members = ctx.guild.members
                found = False
                for i in members:
                    if i.nick == (" ".join(j[1:])):
                        for role in i.roles:
                            if "Hacker" == role.name:
                                found = True
                if found == False:
                    # send message about being verified
                    await ctx.send("You have been verified", delete_after=3.0)
                    # perms
                    await ctx.author.edit(nick=" ".join(j[1:]))
                    role = discord.utils.get(ctx.guild.roles, name="Hacker")
                    await ctx.author.add_roles(role)
                if found == True:
                    await ctx.send(
                        "This email has already been used. If this is an error, please contact @Himanish",
                        delete_after=3.0,
                    )
                break

    await ctx.message.delete(delay=3.0)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(
            "You must type `!verify your_email_address` into the chat below to be verified.",
            delete_after=3.0,
        )
        await ctx.message.delete(delay=3.0)


@bot.listen()
async def on_message(message):
    split_message = message.content.split()
    if split_message[0] != "!verify" and message.channel.name == "verification":
        await message.delete(delay=3.0)


bot.run(TOKEN)
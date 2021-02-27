# bot.py
import os
import random
from dotenv import load_dotenv
import discord
import re

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
        if name.lower() in (" ".join(j[6:])).lower():
            new_message = (
                "Name: "
                + j[-2]
                + " "
                + j[-1]
                + "\nEmail: "
                + j[0]
                + "\nGender: "
                + j[1]
                + "\nEthnicity: "
                + j[2]
                + "\nSchool: "
                + re.sub(r"([A-Z])", r" \1", j[3])
                + "\nStudy level and Graduation: "
                + " ".join(j[4:6])
            )
            # create an @ for them in the channel
            members = ctx.guild.members
            new_message2 = new_message
            for i in members:
                if i.nick == " ".join(j[6:]):
                    new_message2 = new_message + "\n" + i.mention
            await ctx.send(new_message2)


@bot.command(name="verify", pass_context=True)
async def verify(ctx, email_address):

    already_verified = False
    # check if user is already verified
    for role in ctx.author.roles:
        if (
            "Hacker" == role.name
            or "IEEE" == role.name
            or "Sponsor" == role.name
            or "Mentor" == role.name
        ):
            already_verified = True
            await ctx.send(
                "You cannot use this command as you have already been verified.",
                delete_after=4.0,
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

        sponsors_arr = []
        with open("sponsors.txt") as f:
            sponsors_arr = f.read().splitlines()

        mentors_arr = []
        with open("mentors.txt") as f:
            mentors_arr = f.read().splitlines()

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
                    await ctx.send("You have been verified", delete_after=4.0)
                    # perms
                    await ctx.author.edit(nick=j[-1] + " (" + " ".join(j[1:-1]) + ")")
                    role = discord.utils.get(ctx.guild.roles, name="IEEE")
                    await ctx.author.add_roles(role)
                    role = discord.utils.get(ctx.guild.roles, name=" ".join(j[1:-1]))
                    await ctx.author.add_roles(role)
                if found == True:
                    await ctx.send(
                        "This email has already been used. If this is an error, please contact @Himanish",
                        delete_after=4.0,
                    )
                break

        # Checking for sponsors
        for i in sponsors_arr:
            j = i.split()
            if j[0].lower() == email_address.lower():
                # check if user already exists
                members = ctx.guild.members
                found = False
                for i in members:
                    if i.nick == (
                        j[1].replace("_", " ") + " (" + " ".join(j[2:]) + ")"
                    ):
                        for role in i.roles:
                            if "Sponsor" == role.name:
                                found = True
                if found == False:
                    # send message about being verified
                    await ctx.send("You have been verified", delete_after=4.0)
                    # perms
                    await ctx.author.edit(
                        nick=j[1].replace("_", " ") + " (" + " ".join(j[2:]) + ")"
                    )
                    role = discord.utils.get(ctx.guild.roles, name="Sponsor")
                    await ctx.author.add_roles(role)
                if found == True:
                    await ctx.send(
                        "This email has already been used. If this is an error, please contact @Himanish",
                        delete_after=4.0,
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
                    if i.nick == (" ".join(j[6:])):
                        for role in i.roles:
                            if "Hacker" == role.name:
                                found = True
                if found == False:
                    # send message about being verified
                    await ctx.send("You have been verified", delete_after=4.0)
                    # perms
                    await ctx.author.edit(nick=" ".join(j[6:]))
                    role = discord.utils.get(ctx.guild.roles, name="Hacker")
                    await ctx.author.add_roles(role)
                if found == True:
                    await ctx.send(
                        "This email has already been used. If this is an error, please contact @Himanish",
                        delete_after=4.0,
                    )
                break

        # check for mentors
        for i in mentors_arr:
            j = i.split()
            if j[0].lower() == email_address.lower():
                # check if user already exists
                members = ctx.guild.members
                found = False
                for i in members:
                    if i.nick == (j[-1] + " (Mentor)"):
                        for role in i.roles:
                            if "Mentor" == role.name:
                                found = True
                if found == False:
                    # send message about being verified
                    await ctx.send("You have been verified", delete_after=4.0)
                    # perms
                    await ctx.author.edit(nick=j[-1] + " (Mentor)")
                    role = discord.utils.get(ctx.guild.roles, name="Mentor")
                    await ctx.author.add_roles(role)
                if found == True:
                    await ctx.send(
                        "This email has already been used. If this is an error, please contact @Himanish",
                        delete_after=4.0,
                    )
                break

    await ctx.message.delete(delay=4.0)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        if ctx.message.content == "!verify":
            await ctx.send(
                "You must type `!verify your_email_address` into the chat below to be verified.",
                delete_after=4.0,
            )
            await ctx.message.delete(delay=4.0)


@bot.listen()
async def on_message(message):
    split_message = message.content.split()
    if split_message[0] != "!verify" and message.channel.name == "verification":
        await message.delete(delay=4.0)


bot.load_extension("announcements")

bot.run(TOKEN)
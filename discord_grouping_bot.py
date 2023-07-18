import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import os

load_dotenv()  # loads environment variables from the .env file

# Set up the bot with the required intents
intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!",  intents=intents)

# Hardcoded voice channel names and URLs
# TODO: Make this automatically get the voice channel names and URLs via the Discord API
# User should be able to specify the voice channel names and return the URLs for each voice channel via command
# User experience issue with Discord bot commands where its difficult to specify multiple different groups of arguments making it complicated to use. 
# Tried previously using Greedy Class to get channels but voice channel is not supported.
VOICE_CHANNEL_LINKS = {
    ":pirate_flag: Pirates": os.getenv('PIRATES_CHANNEL_URL'),
    ":crossed_swords: Vikings": os.getenv('VIKINGS_CHANNEL_URL'),
    ":japanese_ogre: Goblins": os.getenv('GOBLINS_CHANNEL_URL'),
    ":crocodile: Crocs": os.getenv('CROCS_CHANNEL_URL')
}

# Defines bot command and arguments
@bot.command()
async def make_groups(ctx, roles: commands.Greedy[discord.Role] = None, *days):
    # If the user typed "help" as the first argument or didn't pass in enough arguments
    if roles is None or (len(roles) == 1 and roles[0].name.lower() == "help"):
        embed = discord.Embed(title="**Help: make_groups**", color=discord.Color.blue())
        embed.add_field(name="Usage", value="`!make_groups [@role1, @role2, ...] [group1, group2, ...]`", inline=False)
        embed.add_field(name="Description", value="It's super confusing but, this creates groups from the specified roles and assigns them to the specified groups. The groups are randomly shuffled for each subsequent group. My head hurts just thinking about it.", inline=False)
        await ctx.send(embed=embed)
        return

    members = []
    for role in roles:
        # Find members with each role
        for member in ctx.guild.members:
            if role in member.roles and not member.bot:
                members.append(member)

    # Remove duplicate members
    members = list(set(members))

    print(f"Found {len(members)} members in the specified roles.")  # Debug information

    # Calculate the group size
    group_size = len(members) // len(VOICE_CHANNEL_LINKS)

    if group_size == 0:
        print("Group size is zero. Not enough members or too many voice channels.")  # Debug information
        return

    # Create the groups
    random.shuffle(members)  # This ensures that the groups are random
    groups = [members[n:n+group_size]
              for n in range(0, len(members), group_size)]

    remaining_members = members[len(groups) * group_size:]  # Members that are left after creating the groups

    # Distribute remaining members evenly
    for i, member in enumerate(remaining_members):
        groups[i % len(groups)].append(member)

    # Create an embed (visuals) for the message
    embed = discord.Embed(title="**Socials for the week**", color=discord.Color.blue())

    # For each day provided in the command, assign and send the groups to a voice channel
    for day_index, day in enumerate(days):
        random.shuffle(members)  # Randomize the members for each day
        groups = [members[n:n+group_size]
                  for n in range(0, len(members), group_size)]

        remaining_members = members[len(groups) * group_size:]  # Returns Members that are leftover after creating the groups

        # Distribute remaining members evenly
        for i, member in enumerate(remaining_members):
            groups[i % len(groups)].append(member)

        embed_text = ""
        for i, group in enumerate(groups):
            channel_name = list(VOICE_CHANNEL_LINKS.keys())[i % len(VOICE_CHANNEL_LINKS)]
            channel_url = VOICE_CHANNEL_LINKS[channel_name]
            group_names = ", ".join(member.nick if member.nick else member.name for member in group)
            embed_text += f"[{channel_name}]({channel_url})\n{group_names}\n\n"
        embed.add_field(name=f"{day}", value=embed_text, inline=False)
        if day_index != len(days) - 1:  # Avoid adding a line after the last day
            embed.add_field(name="\u200b", value="~" * 60, inline=False)  # Add a line of hyphens
        random.shuffle(groups)  # Randomize the groups for the next day

    # Send the embed
    await ctx.send(embed=embed)

# some additional catch all error handling
@make_groups.error
async def make_groups_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="**Error: You're missing something!**", color=discord.Color.red())
        embed.add_field(name="Usage", value="`!make_groups [@role1, @role2, ...] [group1, group2, ...]`", inline=False)
        embed.add_field(name="Description", value="It's super confusing but, this creates groups from the specified roles and assigns them to the specified groups. The groups are randomly shuffled for each subsequent group. My head hurts just thinking about it", inline=False)
        await ctx.send(embed=embed)

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
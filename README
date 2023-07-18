# Discord Group Maker Bot

This is a simple Discord bot that allows a server admin or a user with appropriate permissions to randomize and assign server members to different voice channels each day.
It was used to randomly set up remote socials each morning for teams using Discord.

## Features

* The bot assigns members of specified roles to voice channels, each day in a week.
* The groups of members and their corresponding channels are randomized daily.
* The bot provides help and error messages to guide users through its usage.
* Environment Variables

You need to provide the following environment variables in a .env file:

* DISCORD_BOT_TOKEN=your_bot_token
* PIRATES_CHANNEL_URL=your_discord_channel_url
* VIKINGS_CHANNEL_URL=your_discord_channel_url
* GOBLINS_CHANNEL_URL=your_discord_channel_url
* CROCS_CHANNEL_URL=your_discord_channel_url

Replace your_bot_token with your actual Discord bot token and your_discord_channel_url with your actual Discord channel URLs.
Note: channel names and their channel links are simply hardcoded in this current iteration.

## Commands

!make_groups [@role1, @role2, ...] [day1, day2, ...]: This command creates groups from the specified roles and assigns them to the specified days. The groups are randomly shuffled for each subsequent day.

## Installation and Usage

1. Clone this repository.
2. Install the required Python packages: pip install -r requirements.txt
3. Create and set up the .env file as described above.
4. Run the bot: python bot.py

## Dependencies

Python 3.8 or later
discord.py
python-dotenv

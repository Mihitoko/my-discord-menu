import discord
from discord.ext import commands
from menu import MyMenu

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', help_command=None, intents=intents)


@client.command()
async def my_menu(ctx):
    x = [discord.Embed(title="Page 2", color=discord.Color.red()).add_field(name="Hello", value="im page two"),
         discord.Embed(title="Page 3", color=discord.Color.gold()).add_field(name="Hello", value="im page three")]
    menu = MyMenu(client, ctx, color=000000)
    menu.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    menu.add_field(name="My menu", value="react to switch page")
    menu.add_embeds(x)
    await menu.start()

client.run("TOKEN")

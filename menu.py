import discord
import asyncio

"""
This class provides a small Embed menu system.
It can only be used in commands where a valid context is given.
"""


class MyMenu(discord.Embed):
    def __init__(self, client: discord.Client, ctx, **kwargs):
        super().__init__(**kwargs)  # calls __init__ from superclass
        self.client = client
        self.ctx = ctx
        self.embeds = [self]  # The first page in the menu is everytime the embed provided by the superclass
        self.max_len = 0
        self.index = 0
        self.delete = kwargs.get('delete', False)  # Specifies if the author should be able to to remove the embed
        self.timeout = kwargs.get('timeout', 60)  # Specifies the wait_for timeout defaults to 60 seconds
        self.emoji_left = kwargs.get('emoji_left', "⏪")
        self.emoji_right = kwargs.get("emoji_right", "⏩")

    async def start(self):  # Starts the menu. Sends the first page and starts to listen to reactions
        emotes = [self.emoji_left, self.emoji_right]
        try:
            message = await self.ctx.send(embed=self.embeds[self.index])
            await message.add_reaction(self.emoji_left)
            await message.add_reaction(self.emoji_right)
            if self.delete:
                await message.add_reaction("🚫")
                emotes.append("🚫")
        except discord.Forbidden:
            return

        def check(reaction, user):
            return user.bot is False and user.id == self.ctx.author.id and reaction.emoji in emotes

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=self.timeout, check=check)
            except asyncio.TimeoutError:
                break

            switch = {self.emoji_right: self.move_right, self.emoji_left: self.move_left}
            try:
                execute = switch[reaction.emoji]
                execute()
                await reaction.remove(user)
            except (discord.Forbidden, KeyError) as e:
                if isinstance(e, KeyError):
                    await message.delete()
                    return
                pass
            await message.edit(embed=self.embeds[self.index])

    def move_right(self):
        if self.index == self.max_len:
            self.index = 0
        else:
            self.index += 1

    def move_left(self):
        if self.index == 0:
            self.index = self.max_len
        else:
            self.index -= 1

    def add_pages(self, embed):  # Adding embeds to the menu. Parameter must be a list
        for i in embed:
            if isinstance(i, discord.Embed):
                self.embeds.append(i)
                self.max_len += 1
            else:
                x = self.from_dict(i)  # Converts embed dictionary's to discord.Embed objekts
                self.embeds.append(x)
                self.max_len += 1

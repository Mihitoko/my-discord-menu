import asyncio

import discord

from menu import MyMenu


class Button:
    def __init__(self, menu, emoji, callback):
        self.menu: CustomMenu = menu  # the menu the button belongs to
        self.emoji = emoji  # the emoji this button represents
        self.callback = callback  # callback when the button triggers

    async def press(self, reaction, user):
        return await self.callback(self, reaction, user)


class CustomMenu(MyMenu):

    def __init__(self, client, ctx, **kwargs):
        super().__init__(client, ctx, **kwargs)
        self.message: discord.Message or None = None  # This stores the message that is created after the menu starts
        self.buttons = {}  # A mapping of all buttons this menu has
        self.topics = {}  # A mapping of all topics and child pages provided
        self._active = True

    def button(self, emoji):  # decorator func to add a button and bind a callback to it
        def decorator(func):
            self.buttons.update({emoji: Button(self, emoji, func)})
            return None

        return decorator

    async def start(self):
        msg = await self.ctx.send(embed=self)
        self.message = msg
        for key, value in self.buttons.items():
            await msg.add_reaction(key)

        def check(reaction, user):
            return user.bot is False and user.id == self.ctx.author.id and reaction.emoji in self.buttons

        while self._active:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=self.timeout, check=check)
                button = self.buttons[reaction.emoji]

                await button.press(reaction, user)

            except asyncio.TimeoutError:
                break

    def stop(self):
        self._active = False

    def set_topic(self, topic, pages=None):
        if pages is None:
            pages = []
        self.topics.update({topic: pages})

    def search_tag(self, tag):
        for topic in self.topics:
            index = 0
            for page in self.topics[topic]:
                if not isinstance(page, Page):
                    continue
                if page.tag == tag:
                    return topic, index
                index += 1
        raise TagNotFoundError(tag)


class Page(discord.Embed):
    def __init__(self, tag=None, **kwargs):
        super().__init__(**kwargs)
        self.tag = tag


class TagNotFoundError(Exception):
    def __init__(self, name=None):
        self.name = name

    def __str__(self):
        return f"Tag {self.name} not found"

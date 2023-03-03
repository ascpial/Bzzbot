"""
Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""

import random
from datetime import datetime

import discord
from discord.ext import commands
from utils import Gunibot, MyContext

from typing import Union

class Misc(commands.Cog):

    CONTAINS_TIMESTAMP = Union[
        int,
        discord.User,
        discord.TextChannel,
        discord.VoiceChannel,
        discord.StageChannel,
        discord.GroupChannel,
        discord.Message,
        discord.Emoji,
        discord.Guild,
    ]

    def __init__(self, bot: Gunibot):
        self.bot = bot
        self.file = "misc"

    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
    # 🍪 Cookie
    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

    @commands.command(name="cookie", aliases=["🍪"])
    @commands.guild_only()
    async def cookie(self, ctx: MyContext, *, user: discord.User = None):
        """La commande la plus utile du monde : donner un cookie à quelqu'un."""

        # If the cookie is given
        if user:
            message = await self.bot._(
                ctx.guild.id,
                "misc.cookie.give",
                to=user.mention,
                giver=ctx.author.mention,
            )

        # If the cookie is for the the command sender
        else:
            message = await self.bot._(
                ctx.guild.id, "misc.cookie.self", to=ctx.author.mention
            )

        # # Creating a webhook that makes reference to villagers of Element Animation
        webhook: discord.Webhook = await ctx.channel.create_webhook(
            name=f"Villager #{random.randint(1, 9)}"
        )

        # Sending the message
        await webhook.send(
            content=message,
            avatar_url="https://d31sxl6qgne2yj.cloudfront.net/wordpress/wp-content/uploads/20190121140737/Minecraft-Villager-Head.jpg",
        )

        # Cleaning webhook & command
        await webhook.delete()
        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass

    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
    # 🪙 Flip a coin
    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

    @commands.command(name="flipacoin", aliases=["fc","coin","🪙"])
    async def flip(self, ctx: MyContext):
        """Fait un pile ou face"""

        a = random.randint(-100, 100)

        # The sign of the number define the result. 0 correspond to the side of the coin
        if a > 0:
            description = await self.bot._(ctx.guild.id, "misc.flipacoin.tails")
        elif a < 0:
            description = await self.bot._(ctx.guild.id, "misc.flipacoin.heads")
        else:
            description = await self.bot._(ctx.guild.id, "misc.flipacoin.side")

        # Building the result messge
        embed = discord.Embed(
            title=await self.bot._(ctx.guild.id, "misc.flipacoin.title"),
            description=description,
            colour=0x2F3136,
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/867/867351.png")

        await ctx.send(embed = embed)

    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
    # 🎲 Roll a dice
    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

    @commands.command(name="rolladice", aliases=["rad","dice","🎲"])
    async def rolladice(self, ctx: MyContext, *, dice:int = 6):
        """Lance un dé

        Il est possible de spécifier le nombre de face de ce dé.
        """

        # Test if the parameter is an integer
        try:
            dice = int(dice)
        except:
            embed = discord.Embed(
                description=await self.bot._(ctx.guild.id, "misc.dice.error.not_int"),
                colour=0xe74c3c,
            )
            embed.set_author(name="Error", icon_url="https://cdn-icons-png.flaticon.com/512/738/738884.png")
            ctx.send(embed=embed)

        # Test if the parameter is upper than 0
        if dice <= 0:
            embed = discord.Embed(
                description=await self.bot._(ctx.guild.id, "misc.dice.error.not_positive"),
                colour=0xe74c3c,
            )
            embed.set_author(name="Error", icon_url="https://cdn-icons-png.flaticon.com/512/738/738884.png")
            ctx.send(embed=embed)

        # Generate the random value and print it
        value = random.randint(1, dice)

        # Building the result message
        embed = discord.Embed(
            title=await self.bot._(ctx.guild.id, "misc.dice.title"),
            description=await self.bot._(ctx.guild.id, "misc.dice.description", value=value),
            colour=0x2F3136,
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055855.png")

        await ctx.send(embed = embed)

    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
    # ❓ dataja
    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

    @commands.command(name="dataja", aliases=["data", "ask", "❓"])
    async def dataja(self, ctx: MyContext):
        """Ne demande pas si tu peux demander, demande juste"""

        embed = discord.Embed(
            title=await self.bot._(ctx.guild.id, "misc.dataja.title"),
            description=await self.bot._(ctx.guild.id, "misc.dataja.description"),
            colour=0x2F3136,
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1180/1180260.png")
        
        await ctx.send(embed = embed)

        # Deleting command
        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass

    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
    # 🗡️ kill
    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

    @commands.command(name="kill", aliases=["🗡️"])
    async def kill(self, ctx: MyContext, *, target: str = None):
        """Tu veux tuer quelqu'un  ? Respire un coup."""

        # Suicide
        if target is None:
            victime = ctx.author.display_name
            ex = ctx.author.display_name.replace(" ", "\\_")

        # Murder
        else:
            victime = target
            ex = target.replace(" ", "\\_")

        author = ctx.author.mention
        tries = 0

        # Generating a random answer
        msg = "misc.kills"
        while msg.startswith("misc.kills") or (
                "{0}" in msg
                and target is None
                and tries < 50
            ):
            choice = random.randint(0, 23)
            msg = await self.bot._(ctx.channel, f"misc.kills.{choice}")
            tries += 1

        footer = self.bot._(ctx.channel, f"misc.kills.footer")

        # Building the result message
        embed = discord.Embed(
            description=msg.format(author, victime, ex),
            colour=0x2F3136,
            footer=footer
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3074/3074476.png")
        
        # Send it
        await ctx.send(
            embed=embed,
            allowed_mentions=discord.AllowedMentions.none(),
        )

    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
    # ⌚ Timestamp
    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖

    @commands.group(name="timestamp")
    async def timestamp(self, ctx: MyContext):
        """Affiche des dates directement dans Discord"""
        if not ctx.subcommand_passed:
            await ctx.author.send(await self.bot._(ctx, "misc.timestamp.help"))

    @timestamp.command(name="get")
    async def get(self, ctx: MyContext, snowflake: CONTAINS_TIMESTAMP = None):
        """If you want to know how old is a thing

        Supported args :
        • Discord ID
        • User mention
        • Channel mention
        • Message link
        • Custom emoji
        """
        if isinstance(snowflake, int):
            source = f"`{snowflake}`"
        elif isinstance(snowflake, (discord.User, discord.abc.GuildChannel)):
            source = snowflake.mention
            snowflake = snowflake.id
        elif isinstance(snowflake, discord.Message):
            source = snowflake.jump_url
            snowflake = snowflake.id
        elif isinstance(snowflake, discord.Emoji):
            source = snowflake
            snowflake = snowflake.id
        elif isinstance(snowflake, discord.Guild):
            source = snowflake.name
            snowflake = snowflake.id
        elif snowflake is None:  # we get the user id
            source = ctx.author.mention
            snowflake = ctx.author.id
        else:
            await ctx.send(
                await self.bot._(
                    ctx.guild.id, "misc.timestamp.not-found", source=snowflake
                )
            )
            return
        timestamp = ((snowflake >> 22) + 1420070400000) // 1000
        await ctx.send(
            await self.bot._(
                ctx.guild.id,
                "misc.timestamp.read-result",
                source=source,
                timestamp=timestamp,
            ),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=False, roles=False
            ),
        )

    @timestamp.command(name="create")
    async def create(
        self,
        ctx: MyContext,
        year: int,
        month: int = 1,
        day: int = 1,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ):
        """Show the timestamp for the specified date"""
        date = datetime(year, month, day, hour, minute, second)
        timestamp = int(date.timestamp())
        await ctx.send(
            await self.bot._(ctx, "misc.timestamp.create-result", timestamp=timestamp)
        )


# The end.
config = {}
async def setup(bot:Gunibot=None, plugin_config:dict=None):
    if bot is not None:
        await bot.add_cog(Misc(bot), icon="🍪")
    if plugin_config is not None:
        global config
        config.update(plugin_config)


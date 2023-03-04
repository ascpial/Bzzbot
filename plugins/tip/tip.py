"""
Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""

import datetime
import io

from PIL import Image
import discord
from discord import app_commands
from discord.ext import tasks, commands
from utils import Gunibot, MyContext

import core

from .months import MOIS
from .floraisons import COULEURS, FLEURS

async def setup(bot:Gunibot):
    tip_plugin = Tips(bot)
    await bot.add_cog(tip_plugin, icon='🐝')
    await tip_plugin.load_emojis()

bot_color = 0xfdc800

NOMS_MOIS = [
    'Janvier',
    'Février',
    'Mars',
    'Avril',
    'Mai',
    'Juin',
    'Juillet',
    'Août',
    'Septembre',
    'Octobre',
    'Novembre',
    'Décembre',
]

EMOJIS_PREFIX = 'pelote_'

class Tips(commands.Cog):
    def __init__(self, bot: Gunibot):
        self.bot = bot
        self.file = "tip"
        self.emoji_guild_id = core.config.get('tip')['emoji_server']

        self.emojis_colors: dict[str, discord.Emoji] = {}
    
    def get_calendar_embed(self, mois: int) -> discord.Embed:
        data = MOIS[mois-1]
        
        embed = discord.Embed(
            color=bot_color,
            title=f"Que faire au Rucher en {NOMS_MOIS[mois-1]} ?",
            description=f"Voici quelques conseils :\n{data['text']}",
            url=data['url'],
        )
        embed.set_footer(text="Clique sur le titre pour en savoir plus !")
        embed.set_image(url=data['image'])

        return embed
    
    def get_floraison_embed(self, mois: int = None) -> discord.Embed:
        if mois is not None:
            content = "\n".join(
                [fleur.to_str(self.emojis_colors) for fleur in FLEURS if fleur.en_floraison(mois)]
            )
        else:
            content = "\n".join(
                [fleur.to_str(self.emojis_colors) for fleur in FLEURS]
            )

        return discord.Embed(
            title=f"Floraisons en {NOMS_MOIS[mois-1]}" if mois is not None else "Floraisons à l'année",
            description=content,
            color=bot_color,
        ).set_thumbnail(
            url="https://media.discordapp.net/attachments/1074313227082665994/1081540663163768892/image_floraison.jpg"
        )

    async def load_emojis(self):
        # vérifie que les emojis sont bien présents sur le serveur spécifié dans la configuration
        emoji_guild = self.bot.get_guild(self.emoji_guild_id)
        if emoji_guild is None:
            print("The emoji guild coulnd not be found, emojis will not works in tip plugin.")
            return
        
        required_emojis = [EMOJIS_PREFIX + couleur.lower() for couleur in COULEURS]
        emojis_colors = {}

        for emoji in emoji_guild.emojis:
            if emoji.name in required_emojis:
                color_name = emoji.name.upper()[len(EMOJIS_PREFIX):]
                emojis_colors[color_name] = emoji
                required_emojis.remove(emoji.name)
        
        if len(required_emojis) > 0:
            for emoji_name in required_emojis:
                buffer = io.BytesIO()
                Image.new(
                    'RGB',
                    (100, 100),
                    COULEURS[emoji_name.upper()[len(EMOJIS_PREFIX):]],
                ).save(buffer, 'PNG')
                buffer.seek(0)
                data = buffer.read()

                new_emoji = await emoji_guild.create_custom_emoji(
                    name=emoji_name.lower(),
                    image=data,
                    reason="Auto emoji upload"
                )
                emojis_colors[emoji_name.upper()[len(EMOJIS_PREFIX):]] = new_emoji
            print(f"Created {len(required_emojis)} emojis for tip plugin")
        
        self.emojis_colors = emojis_colors
        print("Loaded emojis for tip plugin!")

    @app_commands.command(
        name='calendrier',
        description="Envoie un résumé de ce qu'il se passe et faut faire pendant un mois",
    )
    @app_commands.describe(
        mois='Choisis pour quel mois tu veux le résumé',
    )
    @app_commands.choices(
        mois=[
            app_commands.Choice(name=mois, value=index+1)
            for index, mois in enumerate(NOMS_MOIS)
        ],
    )
    async def calendar(
        self,
        inter: discord.Interaction,
        mois: int = None,
    ):
        if mois is None:
            mois = datetime.datetime.now().month

        await inter.response.send_message(embed=self.get_calendar_embed(mois))
    
    @app_commands.command(
        name='floraison',
        description="Envoie la liste des plantes en floraison pendant un mois",
    )
    @app_commands.describe(
        mois='Choisis pour quel mois tu veux le résumé',
    )
    @app_commands.choices(
        mois=[
            app_commands.Choice(name=mois, value=index+1)
            for index, mois in enumerate(NOMS_MOIS)
        ],
    )
    async def floraison(
        self,
        inter: discord.Interaction,
        mois: int = None,
    ):
        await inter.response.send_message(embed=self.get_floraison_embed(mois))

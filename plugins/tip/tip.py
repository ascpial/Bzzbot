"""
Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""

import datetime

import discord
from discord import app_commands
from discord.ext import tasks, commands
from utils import Gunibot, MyContext

from .months import MOIS

async def setup(bot:Gunibot):
    await bot.add_cog(Tips(bot), icon='🐝')

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

class Tips(commands.Cog):
    def __init__(self, bot: Gunibot):
        self.bot = bot
        self.file = "tip"
    
    def get_embed(self, mois: int) -> discord.Embed:
        data = MOIS[mois-1]
        
        embed = discord.Embed(
            color=0xdcba2a,
            title=f"Que faire au Rucher en {NOMS_MOIS[mois-1]} ?",
            description=f"Voici quelques conseils :\n{data['text']}",
            url=data['url'],
        )
        embed.set_footer(text="Clique sur le titre pour en savoir plus !")
        embed.set_image(url=data['image'])

        return embed

    @app_commands.command(
        name='calendrier',
        description="Envoie un résumé de ce qu'il se passe et faut faire pendant un mois",
    )
    @app_commands.describe(
        mois='Choisis pour quel mois tu veux le résumé',
    )
    @app_commands.choices(
        mois=[
            app_commands.Choice(name='Janvier', value=1),
            app_commands.Choice(name='Février', value=2),
            app_commands.Choice(name='Mars', value=3),
            app_commands.Choice(name='Avril', value=4),
            app_commands.Choice(name='Mai', value=5),
            app_commands.Choice(name='Juin', value=6),
            app_commands.Choice(name='Juillet', value=7),
            app_commands.Choice(name='Août', value=8),
            app_commands.Choice(name='Septembre', value=9),
            app_commands.Choice(name='Octobre', value=10),
            app_commands.Choice(name='Novembre', value=11),
            app_commands.Choice(name='Décembre', value=12),
        ]
    )
    async def calendar(
        self,
        inter: discord.Interaction,
        mois: int = None,
    ):
        if mois is None:
            mois = datetime.datetime.now().month

        await inter.response.send_message(embeds=[self.get_embed(mois)])

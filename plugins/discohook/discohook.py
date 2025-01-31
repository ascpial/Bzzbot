"""
Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""

from typing import Union
import base64
import json
import io

import discord
from discord import app_commands
from discord.ext import commands
from utils import Gunibot, MyContext

DISCOHOOK_BASE_LINK = "https://discohook.org/"

def message_to_dict(message=discord.Message):
    data = {
        "content": message.content,
        "flags": message.flags.value,
        "embeds": [embed.to_dict() for embed in message.embeds] if len(message.embeds) > 0 else None,
    }
    for embed_data in data["embeds"]:
        embed_data.pop("type")
    return data

def get_discohook_payload(
    message: discord.Message,
) -> dict:
    if message is None:
        return {
            "messages": [
                {
                    "data": {
                        "content": None,
                        "embeds": None,
                        "attachments": [],
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "data": message_to_dict(message),
                }
            ]
        }

def discohook_link(
    message: discord.Message = None,
):
    content = json.dumps(get_discohook_payload(message))
    
    return DISCOHOOK_BASE_LINK + "?data=" + base64.urlsafe_b64encode(
        bytes(content, encoding='utf-8')
    ).decode()

async def setup(bot:Gunibot):
    await bot.add_cog(Template(bot))

class Template(commands.Cog):
    def __init__(self, bot: Gunibot):
        self.bot = bot
        self.file = "template"

        self.context_edit_message = app_commands.ContextMenu(
            name="Éditer le message",
            callback=self.edit_rich_message,
        )
        self.bot.tree.add_command(self.context_edit_message)

    def get_webhook_url(
        self,
        webhook: discord.Webhook,
        channel: Union[discord.TextChannel, discord.Thread],
    ) -> str:
        if isinstance(channel, discord.Thread):
            return webhook.url + f"?thread_id={channel.id}"
        else:
            return webhook.url

    async def get_webhook(
        self,
        channel: discord.TextChannel | discord.Thread,
    ) -> discord.Webhook:
        if isinstance(channel, discord.Thread):
            main_channel = channel.parent
        else:
            main_channel = channel

        for webhook in await main_channel.webhooks():
            if webhook.user == self.bot.user\
                and webhook.name == self.bot.user.name:
                break
        else:
            webhook = await main_channel.create_webhook(
                name=self.bot.user.name,
                avatar=await self.bot.user.avatar.read(),
                reason="Webhook mandated for Discohook",
            )
        
        return webhook

    @app_commands.command(
        name="rich-message",
        description="Récupère un lien pour envoyer un message avec discohook ici",
    )
    @app_commands.default_permissions(manage_webhooks=True)
    async def rich_message(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=True)

        webhook_url = self.get_webhook_url(
            await self.get_webhook(inter.channel),
            inter.channel,
        )

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Discohook",
                url=discohook_link(),
            )
        )

        await inter.edit_original_response(
            content=await self.bot._(inter.guild.id, 'discohook.open-link')+"\n"\
                f"||<{webhook_url}>||\n",
            view=view,
        )

    @app_commands.default_permissions(manage_webhooks=True)
    async def edit_rich_message(self, inter: discord.Interaction, message: discord.Message):
        await inter.response.defer(ephemeral=True)

        webhook = await self.get_webhook(inter.channel)

        if message.webhook_id == webhook.id:
            edit_message = await self.bot._(inter.guild.id, 'discohook.edit-link') + "\n"\
                f"<{message.jump_url}>"
        else:
            edit_message = await self.bot._(inter.guild.id, 'discohook.cannot-edit')

        webhook_url = self.get_webhook_url(webhook, inter.channel)

        link = discohook_link(message)

        if len(link) > 512: # discord limitation
            edit_message += "\n\n" + await self.bot._(inter.guild.id, 'discohook.load-edit')
            buffer = io.StringIO()
            buffer.write(
                json.dumps(message_to_dict(message))
            )
            buffer.seek(0)
            files = [discord.File(buffer, filename="message-backup.txt")]
            link = discohook_link()
        else:
            files = []

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Discohook",
                url=link,
            )
        )

        await inter.edit_original_response(
            content=await self.bot._(inter.guild.id, 'discohook.open-link')+"\n"\
                f"||<{webhook_url}>||\n\n" + edit_message,
            view=view,
            attachments=files,
        )

"""
Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""

import discord
from discord.ext import commands
from utils import Gunibot, MyContext


class Welcome(commands.Cog):
    def __init__(self, bot: Gunibot):
        self.bot = bot
        self.config_options = [
            "welcome_roles",
            "welcome_channel",
            "departure_channel",
        ]

        bot.get_command("config").add_command(self.config_welcome_roles)
        bot.get_command("config").add_command(self.config_welcome_channel)
        bot.get_command("config").add_command(self.config_departure_channel)

    @commands.command(name="welcome_roles")
    async def config_welcome_roles(
        self, ctx: MyContext, roles: commands.Greedy[discord.Role]
    ):
        if len(roles) == 0:
            roles = None
        else:
            roles = [role.id for role in roles]
        await ctx.send(
            await self.bot.sconfig.edit_config(ctx.guild.id, "welcome_roles", roles)
        )
    
    @commands.command(name="welcome_channel")
    async def config_welcome_channel(
        self, ctx: MyContext, channel: discord.TextChannel,
    ):
        await ctx.send(
            await self.bot.sconfig.edit_config(ctx.guild.id, "welcome_channel", channel.id)
        )
    
    @commands.command(name="departure_channel")
    async def config_departure_channel(
        self, ctx: MyContext, channel: discord.TextChannel,
    ):
        await ctx.send(
            await self.bot.sconfig.edit_config(ctx.guild.id, "departure_channel", channel.id)
        )

    async def give_welcome_roles(self, member: discord.Member):
        g = member.guild
        config = self.bot.server_configs[g.id]
        rolesID = config["welcome_roles"]
        if not rolesID:  # if nothing has been setup
            return
        roles = [g.get_role(x) for x in rolesID]
        pos = g.me.top_role.position
        roles = filter(lambda x: (x is not None) and (x.position < pos), roles)
        await member.add_roles(*roles, reason="New members roles")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Called when a member joins a guild"""
        g = member.guild
        if not g.me.guild_permissions.manage_roles:  # if not allowed to manage roles
            self.bot.log.info(
                f'Module - Welcome: Missing "manage_roles" permission on guild "{g.name}"'
            )
            return
        
        welcome_channel = self.bot.server_configs[g.id].get('welcome_channel', None)
        if welcome_channel is not None:
            channel = self.bot.get_channel(welcome_channel)

            embed = discord.Embed(
                title="Une nouvelle abeille a rejoint la ruche !",
                description=f"""🐝 {member.mention} a rejoint Les Api's ! 🐝

🌷 On espère que tu ne piques pas 🌷""",
                color=0xdcba2a,
            )
            embed.set_image(
                url="https://media.discordapp.net/attachments/1013758012051165187/1081349077360443523/banner.JPG"
            )

            await channel.send(embed=embed)

        if "MEMBER_VERIFICATION_GATE_ENABLED" not in g.features:
            # we give new members roles if the verification gate is disabled
            await self.give_welcome_roles(member)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Main function called when a member got verified in a community server"""
        if before.pending and not after.pending:
            if "MEMBER_VERIFICATION_GATE_ENABLED" in after.guild.features:
                await self.give_welcome_roles(after)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        departure_channel = self.bot.server_configs[member.guild.id].get('departure_channel', None)
        if departure_channel is not None:
            channel = self.bot.get_channel(departure_channel)

            embed = discord.Embed(
                title="Un membre vient de partir 😢",
                description=f"🐝 {member.name} a essaimé ! On espère vite le retrouver en haut d'un arbre auprès de sa reine ! 🐝",
                color=0xdcba2a,
            )
            embed.set_image(
                url="https://media.discordapp.net/attachments/1013758012051165187/1081349077360443523/banner.JPG"
            )

            await channel.send(embed=embed)


config = {}
async def setup(bot:Gunibot=None, plugin_config:dict=None):
    if bot is not None:
        await bot.add_cog(Welcome(bot), icon="👋")
    if plugin_config is not None:
        global config
        config.update(plugin_config)


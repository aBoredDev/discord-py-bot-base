#!/usr/bin/env python3
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, bot):
        """Initalize the cog

        Args:
            bot (commands.Bot): The bot the cog has been added to
        """
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        """
        Returns the bot's latency.

        Args:
            ctx (commands.Context): The invocation context
        """
        await ctx.send(':ping_pong: Pong! ' + str(self.bot.latency*1000) + 'ms')
    
    @commands.group(hidden=True)
    async def list(self, ctx):
        """Lists all the cogs and extensions currently loaded

        Args:
            ctx (commands.Context): The invocation context
        """
        message = '```Cogs:'
        for key in self.bot.cogs.keys():
            message += '\n  ' + str(key)
        message += '```'
        message += '\n```Extensions:'
        for key in self.bot.extensions.keys():
            message += '\n  ' + str(key)
        message += '```'
        await ctx.send(message)

    @list.command()
    async def cogs(self, ctx):
        """List all the cogs currently loaded

        Args:
            ctx (commands.Context): The invocation context
        """
        message = '```Cogs:'
        for key in self.bot.cogs.keys():
            message += '\n  ' + str(key)
        message += '```'
        await ctx.send(message)

    @list.command()
    async def extensions(self, ctx):
        """List all the extensions currently loaded

        Args:
            ctx (commands.Context): The invocation context
        """
        message = '```Extensions:'
        for key in self.bot.extensions.keys():
            message += '\n  ' + str(key)
        message += '```'
        await ctx.send(message)

def setup(bot):
    """Setup the extenstion

    Args:
        bot (commands.bot): The bot to add the extension to
    """
    bot.add_cog(Utility(bot))
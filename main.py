from discord.ext import commands
import asyncio
from pretty_help import PrettyHelp
from json import load, dump


class BotConfig:
    """The basic config settings for the bot
    """
    def __init__(self, configpath='config.json'):
        """The basic config settings for the bot

        Args:
            configpath (str, optional): The path to the config file. Defaults to 'config.json'.
        """
        self.configpath = configpath
        self.extensions = None
        self.owner_id = None
        self.command_prefix = '/'
        self.token = ''
        with open(configpath, 'r') as fp:
            cfg = load(fp)
            self.extensions = cfg['extensions']
            self.owner_id = cfg['owner_id']
            self.command_prefix = cfg['command_prefix']
            self.token = cfg['token']
            fp.close()
    
    def save_config(self):
        with open(configpath, 'w') as fp:
            cfg = {
                "extensions": self.extensions,
                "owner_id": self.owner_id,
                "command_prefix": self.command_prefix,
                "token": self.token
            }
            dump(cfg, fp)
            fp.close()


config = BotConfig()

bot = commands.Bot(command_prefix=config.command_prefix, owner_id=config.owner_id, help_command=PrettyHelp())


def check_owner(ctx):
    return bot.is_owner(ctx.author)


# Events
@bot.event
async def on_connect():
    print('Logged in as', bot.user)
    print('Latency: ' + str(bot.latency*1000) + 'ms')
    print('===============\n')

@bot.event
async def on_ready():
    print('Bot ready!')
    bot.load_extension('commands.utility')
    print('Extension commands.utility loaded')


# Extension management
@bot.command(hidden=True)
@commands.check(check_owner)
async def load(ctx, extension: str):
    """Loads the specified extension

    Args:
        ctx (commands.Context): The invocation context
        extension (str): The name of the extension to load
    """
    try:
        bot.load_extension(extension)
    except ExtensionNotFound:
        await ctx.send(':x: Extension \'' + extension +'\' could not be found!')
    except ExtensionAlreadyLoaded:
        await ctx.send(':x: Extension \'' + extension +'\' already loaded!')
    except ExtensionFailed:
        await ctx.send(':x: Extension \'' + extension +'\' failed during setup!')
    else:
        await ctx.send(':white_check_mark: Extension \'' + extension +'\' loaded successfully!')
        print('Extension', extension, 'loaded!')

@bot.command(hidden=True)
@commands.check(check_owner)
async def unload(ctx, extension: str):
    """Unloads the specified extension

    Args:
        ctx (commands.Context): The invocation context
        extension (str): The name of the extension to unload
    """
    try:
        bot.unload_extension(extension)
    except ExtensionNotLoaded:
        await ctx.send(':x: Extension \'' + extension +'\' was not loaded!')
    else:
        await ctx.send(':white_check_mark: Extension \'' + extension +'\' unloaded successfully!')
        print('Extension', extension, 'unloaded')

@bot.command(hidden=True)
@commands.check(check_owner)
async def reload(ctx, extension: str):
    """Reloads the specified extension

    Args:
        ctx (commands.Context): The invocation context
        extension (str): The name of the extension to reload
    """
    try:
        bot.reload_extension(extension)
    except ExtensionNotFound:
        await ctx.send(':x: Extension \'' + extension +'\' could not be found!')
    except ExtensionNotLoaded:
        await ctx.send(':x: Extension \'' + extension +'\' was not loaded!')
    except ExtensionFailed:
        await ctx.send(':x: Extension \'' + extension +'\' failed during setup!')
    else:
        await ctx.send(':white_check_mark: Extension \'' + extension +'\' reloaded successfully!')
        print('Extension', extension, 'reloaded')


bot.run(config.token)
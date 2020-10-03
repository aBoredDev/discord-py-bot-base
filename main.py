from discord.ext import commands
import asyncio
from pretty_help import PrettyHelp
from json import load, dump
from datetime import datetime, timezone


### Configuration and loging methods ###
def console_log(message, level: int = 0):
    offset = datetime.now() - datetime.utcnow()
    tz = timezone(offset)
    date = datetime.now(tz)
    if level == 0:
        print(date.strftime('[%Y-%M-%d %H:%M:%S.%f UTC%z]'), '[INFO]', message)
    elif level == 1:
        print(date.strftime('[%Y-%M-%d %H:%M:%S.%f UTC%z]'), '[WARNING]', message)
    elif level == 0:
        print(date.strftime('[%Y-%M-%d %H:%M:%S.%f UTC%z]'), '[ERROR]', message)


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
        self.debug = False
        
        with open(self.configpath, 'r') as fp:
            cfg = load(fp)
            self.extensions = cfg['extensions']
            self.owner_id = cfg['owner_id']
            self.command_prefix = cfg['command_prefix']
            self.token = cfg['token']
            self.debug = cfg['debug']
            fp.close()

    def save(self):
        with open(self.configpath, 'w') as fp:
            cfg = load(fp)
            self.extensions = cfg['extensions']
            self.owner_id = cfg['owner_id']
            self.command_prefix = cfg['command_prefix']
            self.token = cfg['token']
            self.debug = cfg['debug']
            fp.close()


### Bot setup ###
config = BotConfig()

bot = commands.Bot(command_prefix=config.command_prefix, owner_id=config.owner_id, help_command=PrettyHelp())


def check_owner(ctx):
    return bot.is_owner(ctx.author)


### Events ###
@bot.event
async def on_connect():
    console_log('Logged in as ' + str(bot.user))
    console_log('Latency: ' + str(bot.latency*1000) + 'ms')
    print('==============================\n')

@bot.event
async def on_ready():
    console_log('Loading extensions...')
    
    for extension in config.extensions:
        try:
            bot.load_extension(extension['name'])
        except ExtensionNotFound:
            console_log('Extension\'' + extension['name'] + '\' could not be found', 1)
        except ExtensionAlreadyLoaded:
            console_log('Extension\'' + extension['name'] + '\' already loaded', 1)
        except ExtensionFailed:
            console_log('Extension\'' + extension['name'] + '\' failed during setup', 2)
            if config.debug:
                raise
        else:
            console_log('Extension\'' + extension['name'] + '\'loaded')
    
    console_log('Bot ready!')
    print('\n==============================\n')


### Commands ###
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
        console_log('Extension\'' + extension + '\' could not be found', 1)
    except ExtensionAlreadyLoaded:
        await ctx.send(':x: Extension \'' + extension +'\' already loaded!')
        console_log('Extension\'' + extension + '\' already loaded', 1)
    except ExtensionFailed:
        await ctx.send(':x: Extension \'' + extension +'\' failed during setup!')
        console_log('Extension\'' + extension + '\' failed during setup', 2)
        if config.debug:
            raise
    else:
        await ctx.send(':white_check_mark: Extension \'' + extension +'\' loaded successfully!')
        console_log('Extension' + extension + 'loaded')

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
        console_log('Extension \'' + extension +'\' was not loaded', 1)
    else:
        await ctx.send(':white_check_mark: Extension \'' + extension + '\' unloaded successfully!')
        console_log('Extension' + extension + 'unloaded')

@bot.command(hidden=True)
@commands.check(check_owner)
async def reload(ctx, extension: str):
    """Reloads the specified extension

    Args:
        extension (str): The name of the extension to reload
    """
    try:
        bot.reload_extension(extension)
    except ExtensionNotFound:
        await ctx.send(':x: Extension \'' + extension +'\' could not be found!')
        console_log('Extension \'' + extension +'\' could not be found!', 1)
    except ExtensionNotLoaded:
        await ctx.send(':x: Extension \'' + extension +'\' was not loaded!')
        console_log('Extension \'' + extension +'\' was not loaded!', 1)
    except ExtensionFailed:
        await ctx.send(':x: Extension \'' + extension +'\' failed during setup!')
        console_log('Extension \'' + extension +'\' failed during setup', 2)
        if config.debug:
            raise
    else:
        await ctx.send(':white_check_mark: Extension \'' + extension +'\' reloaded successfully!')
        console_log('Extension' + extension + 'reloaded')


bot.run(config.token)
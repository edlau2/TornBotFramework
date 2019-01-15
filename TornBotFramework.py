#
# TornBotFramework.py
# A class driven, generic framework to which any command may easily be added.
# To add a new command, simply add the function in the section that has a comment
# that says: "This section is where any new commands can be added"
#
# After adding the function, be sure to register it with the command handler, 
# using the class's add_command() function. That's it. Easy peasy, lemon squeezy.
#
import discord
import requests
import json
import os
import sys

from discord.ext import commands    # Extension handling module

import config                       # Private config file, contains our token

###############################################################################
#
# Command handler class
# Performs the execution of entered commands.
#
###############################################################################

class CommandHandler:

    # constructor
    def __init__(self, bot):
        self.bot = bot
        self.commands = []

    # Adds a command to our list of known commands
    def add_command(self, command):
        self.commands.append(command)

    # The handler itself
    def command_handler(self, message):
        for command in self.commands:
            if message.content.startswith(command['trigger']):
                args = message.content.split(' ')
                if args[0] == command['trigger']:
                    args.pop(0)
                    if command['args_num'] == 0:
                        return self.bot.send_message(message.channel, str(command['function'](message, self.bot, args)))
                        break
                    else:
                        if len(args) >= command['args_num']:
                            return self.bot.send_message(message.channel, str(command['function'](message, self.bot, args)))
                            break
                        else:
                            return self.bot.send_message(message.channel, 'command "{}" requires {} argument(s) "{}"'.format(command['trigger'], command['args_num'], ', '.join(command['args_name'])))
                            break
                else:
                    break

###############################################################################
#
# Extension (cog) manager class
# used to keep track of loaded, unloaded, and available extensions
#
###############################################################################

class ExtensionManager:

    # constructor
    def __init__(self, bot):
        self.bot = bot
        self.loaded_extensions = []
        self.all_extensions = []

    # Loads an extension and add to our lists of known and loaded extensions
    def load_local_extension(self, extension):
        self.all_extensions.append(extension)
        try:
            self.bot.load_extension('cogs.{}'.format(extension))
            print('Loaded extension {}'.format(extension))
        except Exception as e:
            print('Failed to load extension {}: {}'.format(extension, e))
            return
        self.loaded_extensions.append(extension)

    # Unloads (stops) an extension and remove from our list of loaded extensions
    def unload_local_extension(self, extension):
        try:
            self.bot.unload_extension('cogs.{}'.format(extension))
            print('Unloaded extension {}'.format(extension))
        except Exception as e:
            print('Failed to unload extension {}: {}'.format(extension, e))
            return
        self.loaded_extensions.remove(extension)

    # Reloads an extension, or load if not already loaded
    def reload_local_extension(self, extension):
        if extension in self.loaded_extensions:
            self.bot.reload_extension('cogs.{}'.format(extension))
            return 'Extension {} reloaded'.format(extension)
        # not loaded, so just load.
        self.load_local_extension(all_extensions)

    # Lists loaded extensions
    def list_loaded_extensions(self):
        count = 0
        ret = "**Loaded Extensions:**\n"
        for extension in self.loaded_extensions:
            ret += '{}\n'.format(extension)
            count += 1
        if (count == 0):
            ret += '<none>'
        return ret

    # Lists all known extensions
    def list_all_extensions(self):
        ret = "**All known Extensions:**\n"
        for extension in self.all_extensions:
            ret += '{}\n'.format(extension)
        return ret

    def get_extension_commands(self):
        return '\n<Help for all loaded extensions not yet implemented>'

###############################################################################
#
# Create the discord bot, command handler, and extension manager 
#
################################################################################

bot = commands.Bot(command_prefix=config.BOT_CONFIG['prefix'], description='Icarus')
ch = CommandHandler(bot)
xm = ExtensionManager(bot)

# Debugging
print('Current working directory: {}'.format(os.getcwd()))

# Load all found cogs
for extension in os.listdir("cogs"):
    if extension.endswith(".py"):         
         xm.load_local_extension(extension[:-3])

###############################################################################
#
# This section is where any new commands can be added. Can do anything you
# want, just be sure to add to the command handler so it gets executed.
#
# I've followed the convention of inserting this immediately after the
# function itself, see below
#
# ch.add_command({
#    'trigger': '!<name of command>',
#    'function': <name of the function>,
#    'args_num': <number of arrguments the command expects>,
#    'args_name': <name of arguments>,
#    'description': <obvious>
# }) 
#
###############################################################################

##
## Start of the !help command
## Simply lists commands accepted
##
def commands_command(message, bot, args):
    try:
        coms = '**Native Command List**\n'
        count = 0
        for command in ch.commands:
            if (command == '!kill'):
                continue
            count += 1
            coms += '{}.) {} : {}\n'.format(count, command['trigger'], command['description'])

        # Now iterate loaded extensions and see if they support !help
        coms += '\n**Loaded Extensions Command List**'
        coms += xm.get_extension_commands()
        return coms
    except Exception as e:
        print(e)

ch.add_command({
    'trigger': '!help',
    'function': commands_command,
    'args_num': 0,
    'args_name': [],
    'description': 'Prints a list of all the commands!'
})
## end help command

##
## Start of the !Hello comnmand. Just says "Hello" to whatever is args[0]
##
def hello_function(message,bot,args):
    try:
        return '{}, {} says Hello!'.format(args[0], message.author)
    except Exception as e:
        return e

ch.add_command({
    'trigger': '!hello',
    'function': hello_function,
    'args_num': 1,
    'args_name': ['string'],
    'description': 'Will say hello to args[0] from the caller'
})
#end hello command

##
## Start of the !ip command. This is an example of using
## HTTP, which will be usefull for interactimg with the Torn API
##
def ip_command(message, bot, args):
    try:
        req = requests.get('http://ip-api.com/json/{}'.format(args[0]))
        resp = json.loads(req.content.decode())
        if req.status_code == 200:
            if resp['status'] == 'success':
                template = '**{}**\n**IP: **{}\n**City: **{}\n**State: **{}\n**Country: **{}\n**Latitude: **{}\n**Longitude: **{}\n**ISP: **{}'
                out = template.format(args[0], resp['query'], resp['city'], resp['regionName'], resp['country'], resp['lat'], resp['lon'], resp['isp'])
                return out
            elif resp['status'] == 'fail':
                return 'API Request Failed'
        else:
            return 'HTTP Request Failed: Error {}'.format(req.status_code)
    except Exception as e:
        print(e)

ch.add_command({
    'trigger': '!ip',
    'function': ip_command,
    'args_num': 1,
    'args_name': ['IP\Domain'],
    'description': 'Prints information about provided IP/Domain!'
})
## end ip command

# This command *should* stop the bot. Not sure I want this to be in !help, or even here at all.
def kill_function(message,bot,args):
    bot.send_message(message.channel, 'Killing Icarus. Bye!')
    #bot.close()

ch.add_command({
    'trigger': '!kill',
    'function': kill_function,
    'args_num': 0,
    'args_name': ['string'],
    'description': 'Kills the bot.'
})             

###############################################################################
#
# Cog (extension) handling functions
#
###############################################################################

##
## Start of the !scog command, stops (unloads) a cog
##
def scog_function(message,bot,args):
    try:
        ret = '{} is stopping extension {}'.format(message.author, args[0])
        xm.unload_local_extension(args[0])
        ret += '\n{} stopped.'.format(args[0])
        return ret
    except Exception as e:
        return e

ch.add_command({
    'trigger': '!scog',
    'function': scog_function,
    'args_num': 1,
    'args_name': ['string'],
    'description': 'Will stop the extension with the provided name'
})
#end !scog command

##
## Start of the !rcog command, reloads a cog
## [p]reload mycog
##
def rcog_function(message,bot,args):
    try:
        ret = '{} is stopping extension {}'.format(message.author, args[0])
        xm.reload_local_extension(args[0])
        ret += '\n{} reloaded.'.format(args[0])
        return ret
    except Exception as e:
        return e

ch.add_command({
    'trigger': '!rcog',
    'function': rcog_function,
    'args_num': 1,
    'args_name': ['string'],
    'description': 'Will reload the extension with the provided name'
})
#end !rcog command

##
## Start of the !llcog command, lists loaded cogs
##
def llcog_function(message,bot,args):
    try:
        return xm.list_loaded_extensions()
    except Exception as e:
        return e

ch.add_command({
    'trigger': '!llcog',
    'function': llcog_function,
    'args_num': 0,
    'args_name': ['string'],
    'description': 'Will list all loaded extensions'
})
#end !llcog command

##
## Start of the !lcog command, lists all known cogs
##
def lcog_function(message,bot,args):
    try:
         return xm.list_all_extensions()
    except Exception as e:
        return e

ch.add_command({
    'trigger': '!lcog',
    'function': lcog_function,
    'args_num': 0,
    'args_name': ['string'],
    'description': 'Will list all known extensions'
})
#end !lcog command

###############################################################################
#
# bot is ready! This is where messages are processed and routed to the correct 
# command handler code.
#
###############################################################################
@bot.event
async def on_ready():
    try:
        print(bot.user.name)
        print(bot.user.id)
    except Exception as e:
        print(e)

# on new message
@bot.event
async def on_message(message):
    # if the message is from the bot itself ignore it
    if message.author == bot.user:
        pass
    else:
        # try to evaluate with the command handler
        try:
            await ch.command_handler(message)
        # message doesn't contain a command trigger
        except TypeError as e:
            pass
        # generic python error
        except Exception as e:
            print(e)

#
# Start the bot!
#
# Note: the token is stored in a file called config.py
#
bot.run(config.BOT_CONFIG['token'])
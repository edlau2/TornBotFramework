This bot is designed as a framework and example bot that has some basic internal (native)
functionality. It was written and debugged using VS 2017, but that is not a requirement.

It showcases loading extension modules ('cogs'), and can dynamically load, unload and reload 
them.

Cogs should be placed in a subdirectory called 'cogs' underneath where the main file, 
TornBotFramework.py, resides.

The main .py file requires a config file, config.py, which is not included here as it contains 
the secret token required for the bot to run.

config.py:

BOT_CONFIG = {
  "token": "secret token",
  "prefix": "!"
}

A very simple cog that does pretty much nothing is also included to use as a baselene to build off of.

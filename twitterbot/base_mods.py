def on_bot_load(bot):
    disabled = {
        'xkcd': bot.modules.disable_module('xkcd'),
        'fun': bot.modules.disable_module('fun'),
        'translate': bot.modules.disable_module('translate'),
        'random': bot.modules.disable_module('random'),
        'define': bot.modules.disable_module('define')
    }
    for k, v in disabled.items():
        if v is not True:
            bot.room.send_message("(base_mods.on_bot_load) Module not disabled: {0}".format(k))

commands = []

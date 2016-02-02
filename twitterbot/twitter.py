# The commands listed in this file can be read and loaded as a Module into a MetaModule by the load_module() function

# Add necessary import to this file, including:
from Module import Command
import datetime
import string
import random
import SaveIO # For if you want to save and load objects for this module.
save_subdir = 'twitter' # Define a save subdirectory for this Module, must be unique in the project. If this is not set, saves and loads will fail.
# SaveIO.save(<object>, save_subdir, <filename>)  # Saves an object, filename does not need an extension.
# SaveIO.load(save_subdir, <filename>)  # Loads and returns an object, filename does not need an extension.

# def on_bot_load(bot): # This will get called when the bot loads (after your module has been loaded in), use to perform additional setup for this module.
#     pass

# def on_bot_stop(bot): # This will get called when the bot is stopping.
#     pass

# def on_event(event, client, bot): # This will get called on any event (messages, new user entering the room, etc.)
#     pass

# Logic for the commands goes here.
#
# def <command exec name>(cmd, bot, args, msg, event): # cmd refers to the Command you assign this function to
#     return "I'm in test1"
#

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def tweet(cmd, bot, args, msg, event): # cmd refers to the Command you assign this function to
    if len(args)<2:
        return "Not enough arguments."
    try:
        delay = int(args[0])
        if delay < 0:
            return "Can't schedule a tweet in the past."
    except ValueError:
        return "Invalid arguments."
    
    tweet = ' '.join(args[1:])
    if len(tweet) > 144:
        return "Unable to schedule tweet since its length exceeds 144 characters."
    
    tweets = SaveIO.load(save_subdir, 'tweets')
    dt = datetime.datetime.now() + datetime.timedelta(seconds=60*delay)
    id = id_generator()
    tweets[id] = [dt, tweet]
    SaveIO.save(tweets, save_subdir, 'tweets')
    return "scheduled tweet: \n%s \ntime: %s \nid: %s" % (tweet, str(dt), id)
    
    


commands = [  # A list of all Commands in this Module.
    Command( 'tweet', tweet, 'Schedules a tweet. Syntax: $PREFIXtweet <delay> (in minutes) <tweet>', True, False, None, None)
    # Command( '<command name>', <command exec name>, '<help text>' (optional), <needs privilege> (= False), <owner only> (= False), <special arg parsing method>(*) (= None), <aliases> (= None), <allowed chars> (= string.printable), <disallowed chars> (= None) (**) ),
    # ...
]

# (*) <special arg parsing method> = Some commands require a non-default argument parsing method.
# Pass it there when necessary. It must return the array of arguments.

# (**) Allowed and disallowed chars
# You can choose to allow/disallow a specific set of characters in the command's arguments.
# By default, the allowed chars is string.printable (see https://docs.python.org/3/library/string.html#string-constants for string constants).
# If a char is both allowed and disallowed, disallowed has higher importance.
# If allowed_chars is None, all chars are allowed (unless those specified in disallowed_chars).

module_name = "twitter"

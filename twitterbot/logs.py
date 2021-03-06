from Module import Command

def write_log_line(line):
    with open("system.log", "a") as f:
        f.write("{}\n".format(line))

def command_logs(cmd, bot, args, msg, event):
    num_lines = int(args[0]) if len(args) > 0 else 100
    with open("system.log", "r") as f:
        lines = f.readlines()
    return "".join(lines[-num_lines:])

commands = [
    Command("logs", command_logs, "Gets *n* lines of system logs. Syntax: $PREFIXlogs <lines>", False, False, None, None)
]

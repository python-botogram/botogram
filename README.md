## botogram

botogram is a Python microframework for Telegram bots. It aims to provide a
solid base for bots based on the [Telegram Bot API][1]. It's released under
the MIT license.

A simple bot looks like this:

```
import botogram
bot = botogram.create("YOUR-API-KEY")

@bot.command("echo")
def echo_command(chat, args):
    """Echo something to a chat"""
    message = "You must provide a message"
    if len(args) != 0:
        message = " ".join(args)

    chat.send_message(message)

bot.run()
```

[1]: https://core.telegram.org/bots

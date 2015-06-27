## botogram

_A microframework for Telegram bots_

botogram is a MIT-licensed microframework, which aims to simplify the creation
of [Telegram bots][1]. It offers a concise, simple API, which allows you to
spend all your creativity in the bot, without worrying about anything else.

It also provides a robust, fully scalable bot runner process, which will be
able to process fastly high workloads. And as if this isn't enough, it has
builtin support for commands, with an automatically-generated ``/help``
command.

```python
import botogram
bot = botogram.create("YOUR-API-KEY")

@bot.command("hello")
def hello_command(chat, message, args):
    """Say hello to the world!"""
    chat.send("Hello world")

bot.run()
```

You can find the documentation at [botogram.pietroalbini.io][2].

### Installation

botogram is currently in development, so a release doesn't exist yet.  
But if you want to install it anyway, you can clone the repository and install
it with setuptools. Be sure to have Python 3, pip and setuptools installed:

    $ git clone https://github.com/pietroalbini/botogram.git
    $ cd botogram
    $ pip install .

On some Linux systems you might need to wrap the ``pip install`` command with
``sudo``, if you don't have root privileges.

[1]: https://core.telegram.org/bots
[2]: http://botogram.pietroalbini.io/docs

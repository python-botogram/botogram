## botogram [![Build Status](https://img.shields.io/travis/pietroalbini/botogram/master.svg)](https://travis-ci.org/pietroalbini/botogram) [![News channel](https://img.shields.io/badge/telegram_channel-@botogram__framework-0d86d7.svg?style=flat)][channel]

_Just focus on your bots._

botogram is a Python framework, which allows you to focus just on creating your
[Telegram bots][1], without worrying about the underlying Bots API.

While most of the libraries for Telegram out there just wrap the Bots API,
botogram focuses heavily on the development experience, aiming to provide you
the best API possible. Most of the Telegram implementation details are managed
by botogram, so you can just focus on your bot.

```python
import botogram
bot = botogram.create("YOUR-API-KEY")

@bot.command("hello")
def hello_command(chat, message, args):
    """Say hello to the world!"""
    chat.send("Hello world")

if __name__ == "__main__":
    bot.run()
```

You can find the documentation at [botogram.pietroalbini.org][2]. Also, you can
get all the news about botogram in its [Telegram channel][channel].

> Please note botogram currently doesn't support some of the upstream API
> features. All of them will be implemented in botogram 1.0

**Supported Python versions**: 3.4, 3.5  
**License**: MIT

### Installation

You can install easily botogram with pip (be sure to have Python 3.4 or higher
installed):

    $ python3 -m pip install botogram

If you want to install from the source code, you can clone the repository and
install it with setuptools. Be sure to have Python 3.4 (or a newer version),
pip, virtualenv, setuptools and [invoke][3] installed:

    $ git clone https://github.com/pietroalbini/botogram.git
    $ cd botogram
    $ invoke install

On some Linux systems you might need to wrap the ``invoke install`` command with
``sudo``, if you don't have root privileges.

[1]: https://core.telegram.org/bots
[2]: https://botogram.pietroalbini.org/docs
[3]: http://www.pyinvoke.org
[channel]: https://telegram.me/botogram_framework

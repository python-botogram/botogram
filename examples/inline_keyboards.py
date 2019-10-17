# Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER

import botogram

token = input("Insert your API token: ")

bot = botogram.create(token)


@bot.command("start")
def start(chat, message):
    """ Starts the bot!"""
    btns = botogram.Buttons()
    btns[0].callback("Button 1", "button-1")
    btns[0].callback("Button 2", "button-2")
    btns[1].url("Button 3", "https://botogram.dev")
    btns[2].switch_inline_query("Button 4", "Inline query")
    text = (
        "<b>This is an inline keyboard.</b>\n\n"
        "<b>Button 1</b> will edit the message and display a "
        "non-popup message.\n"
        "<b>Button 2</b> will send a new message and display a "
        "popup message.\n"
        "<b>Button 3</b> is a <code>url</code> button.\n"
        "<b>Button 4</b> is a <code>switch inline query</code> button, "
        "will start the bot in inline-mode to a user-chosen chat."
    )
    chat.send(text, attach=btns)


@bot.callback("button-1")
def button_1(query, message, chat):
    query.notify("Non-popup message!")
    message.edit("The message has been edited!")


@bot.callback("button-2")
def button_1(query, message, chat):
    query.notify("Popup message!", alert=True)
    chat.send("A new message has been sent!")


if __name__ == "__main__":
    bot.run()

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



class KeyboardRow:
    """A row of a keyboard"""

    def __init__(self):
        self._content = []

    def text(self, text):
        """Sends a message when the button is pressed"""
        self._content.append({"text": text})

    def request_contact(self, label):
        """Ask the user if he wants to share his contact"""

        self._content.append({
            "text": label,
            "request_contact": True,
        })

    def request_location(self, label):
        """Ask the user if he wants to share his location"""

        self._content.append({
            "text": label,
            "request_location": True,
        })

    def _get_content(self, chat):
        """Get the content of this row"""
        for item in self._content:
            new = item.copy()

            # Replace any callable with its value
            # This allows to dynamically generate field values
            for key, value in new.items():
                if callable(value):
                    new[key] = value(chat)

            yield new


class Keyboard:
    """Factory for keyboards"""

    def __init__(self, resize=False, one_time=False, selective=False):
        self.resize_keyboard = resize
        self.one_time_keyboard = one_time
        self.selective = selective
        self._rows = {}

    def __getitem__(self, index):
        if index not in self._rows:
            self._rows[index] = KeyboardRow()
        return self._rows[index]

    def _serialize_attachment(self, chat):
        rows = [
            list(row._get_content(chat)) for i, row in sorted(
                tuple(self._rows.items()), key=lambda i: i[0]
            )
        ]

        return {"keyboard": rows, "resize_keyboard": self.resize_keyboard,
                "one_time_keyboard": self.one_time_keyboard,
                "selective": self.selective}


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
#   DEALINGS IN THE SOFTWARE.

import botogram
import botogram.tasks


@botogram.pass_bot
def sample_timer(bot=None):
    return bot


def test_timer_now(bot):
    timer = botogram.tasks.TimerTask(5, sample_timer)
    assert timer.now(current=0) == True
    assert timer.now(current=3) == False
    assert timer.now(current=5) == True
    assert timer.now(current=6) == False
    assert timer.now(current=8) == False
    assert timer.now(current=10) == True


def test_timer_process(bot):
    timer = botogram.tasks.TimerTask(5, sample_timer)
    assert timer.process(bot) == bot


def test_scheduler(bot):
    timer1 = botogram.tasks.TimerTask(5, sample_timer)
    timer2 = botogram.tasks.TimerTask(3, sample_timer)

    scheduler = botogram.tasks.Scheduler()
    scheduler.add(timer1)
    scheduler.add(timer2)

    assert list(scheduler.now(current=0)) == [timer1, timer2]
    assert list(scheduler.now(current=2)) == []
    assert list(scheduler.now(current=3)) == [timer2]
    assert list(scheduler.now(current=5)) == [timer1]
    assert list(scheduler.now(current=7)) == [timer2]
    assert list(scheduler.now(current=8)) == []
    assert list(scheduler.now(current=10)) == [timer1, timer2]

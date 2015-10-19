"""
    Tests for botogram/timers.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import botogram
import botogram.timers


@botogram.pass_bot
def sample_timer(bot=None):
    return bot


def test_timer_now(bot):
    timer = botogram.timers.TimerJob(5, bot._bot_id, sample_timer)
    assert timer.now(current=0) == True
    assert timer.now(current=3) == False
    assert timer.now(current=5) == True
    assert timer.now(current=6) == False
    assert timer.now(current=8) == False
    assert timer.now(current=10) == True


def test_timer_process(bot):
    timer = botogram.timers.TimerJob(5, bot._bot_id, sample_timer)
    assert timer.process({bot._bot_id: bot}) == bot


def test_scheduler(bot):
    timer1 = botogram.timers.TimerJob(5, bot._bot_id, sample_timer)
    timer2 = botogram.timers.TimerJob(3, bot._bot_id, sample_timer)

    scheduler = botogram.timers.Scheduler()
    scheduler.add(timer1)
    scheduler.add(timer2)

    assert list(scheduler.now(current=0)) == [timer1, timer2]
    assert list(scheduler.now(current=2)) == []
    assert list(scheduler.now(current=3)) == [timer2]
    assert list(scheduler.now(current=5)) == [timer1]
    assert list(scheduler.now(current=7)) == [timer2]
    assert list(scheduler.now(current=8)) == []
    assert list(scheduler.now(current=10)) == [timer1, timer2]

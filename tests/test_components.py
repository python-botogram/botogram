"""
    Tests for botogram/components.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import copy

import botogram.components


def test_add_before_processing_hook(bot, sample_update):
    # This will be true if the before_processing hook was processed
    before_hook_processed = False
    process_hook_processed = False

    # Configure the test bot
    def before_processing(chat, message):
        nonlocal before_hook_processed
        before_hook_processed = True

        # Test provided arguments are OK
        assert chat.id == -1
        assert message.text == "test"
        assert message.chat == chat

    # This will test if the hook processing order is right
    def process_message(*__):
        nonlocal process_hook_processed
        process_hook_processed = True

        # Should be called after before_processing
        assert before_hook_processed

    component = botogram.components.Component()
    component.add_before_processing_hook(before_processing)
    component.add_process_message_hook(process_message)

    bot.use(component)
    bot.process(sample_update)

    assert before_hook_processed
    assert process_hook_processed


def test_add_process_message_hook(bot, sample_update):
    # This will be true if the process_message hook was processed
    process_hook_processed = False

    # Configure the test bot
    def process_message(chat, message):
        nonlocal process_hook_processed
        process_hook_processed = True

        # Test provided arguments are OK
        assert chat.id == -1
        assert message.text == "test"
        assert message.chat == chat

    component = botogram.components.Component()
    component.add_process_message_hook(process_message)

    bot.use(component)
    bot.process(sample_update)

    assert process_hook_processed


def test_add_message_equals_hook(bot, sample_update):
    # meanings: ins[ensitive], sen[sitive], rig[ht], wro[ng]
    ins_wro_processed = False
    ins_rig_processed = False
    sen_wro_processed = False
    sen_rig_processed = False

    def ins_wro_hook(chat, message):
        nonlocal ins_wro_processed
        ins_wro_processed = True

    def ins_rig_hook(chat, message):
        nonlocal ins_rig_processed
        ins_rig_processed = True

        assert chat.id == -1
        assert message.text == "test"

    def sen_wro_hook(chat, message):
        nonlocal sen_wro_processed
        sen_wro_processed = True

    def sen_rig_hook(chat, message):
        nonlocal sen_rig_processed
        sen_rig_processed = True

    ins_comp = botogram.components.Component("ins")
    ins_comp.add_message_equals_hook("hi", ins_wro_hook)
    ins_comp.add_message_equals_hook("Test", ins_rig_hook)

    sen_comp = botogram.components.Component("sen")
    sen_comp.add_message_equals_hook("Test", sen_wro_hook, ignore_case=False)
    sen_comp.add_message_equals_hook("test", sen_rig_hook, ignore_case=False)

    for comp in ins_comp, sen_comp:
        localbot = copy.copy(bot)
        localbot.use(comp)
        localbot.process(sample_update)

    assert ins_wro_processed == False
    assert sen_wro_processed == False
    assert ins_rig_processed == True
    assert sen_rig_processed == True


def test_add_message_contains_hook(bot, sample_update):
    # meanings: ins[ensitive], sen[sitive], rig[ht], wro[ng]
    ins_wro_processed = False
    ins_rig_processed = False
    sen_wro_processed = False
    sen_rig_processed = False
    single_processed = 0
    multiple_processed = 0

    def ins_wro(chat, message):
        nonlocal ins_wro_processed
        ins_wro_processed = True

    def ins_rig(chat, message):
        nonlocal ins_rig_processed, single_processed
        ins_rig_processed = True
        single_processed += 1

        assert chat.id == -1
        assert message.text == "test test test"
        assert message.chat == chat

    def sen_wro(chat, message):
        nonlocal sen_wro_processed
        sen_wro_processed = True

    def sen_rig(chat, message):
        nonlocal sen_rig_processed
        sen_rig_processed = True

    def multiple(chat, message):
        nonlocal multiple_processed
        multiple_processed += 1

    comp1 = botogram.Component("ins")
    comp1.add_message_contains_hook("hi", ins_wro)
    comp1.add_message_contains_hook("test", ins_rig)

    comp2 = botogram.Component("sen")
    comp2.add_message_contains_hook("Test", sen_wro, ignore_case=False)
    comp2.add_message_contains_hook("test", sen_rig, ignore_case=False)

    comp3 = botogram.Component("multiple")
    comp3.add_message_contains_hook("test", multiple, multiple=True)

    sample_update.message.text = "test test test"

    for comp in comp1, comp2, comp3:
        localbot = copy.copy(bot)
        localbot.use(comp)
        localbot.process(sample_update)

    assert ins_wro_processed == False
    assert ins_rig_processed == True
    assert sen_wro_processed == False
    assert sen_rig_processed == True
    assert single_processed == 1
    assert multiple_processed == 3


def test_add_message_matches_hook(bot, sample_update):
    # meanings: ins[ensitive], sen[sitive], rig[ht], wro[ng]
    wrong_processed = False
    right_processed = False
    single_processed = 0
    multiple_processed = 0

    def wrong(chat, message, matches):
        nonlocal wrong_processed
        wrong_processed = True

    def right(chat, message, matches):
        nonlocal right_processed, single_processed
        right_processed = True
        single_processed += 1

        assert chat.id == -1
        assert message.text == "a_b_c c_a_b b_c_a"
        assert message.chat == chat
        assert matches == ('a', 'b', 'c')

    def multiple(chat, message, matches):
        nonlocal multiple_processed
        multiple_processed += 1

    comp1 = botogram.Component("single")
    comp1.add_message_matches_hook(r"([a-c])\-([a-c])\-([a-c])", wrong)
    comp1.add_message_matches_hook(r"([a-c])_([a-c])_([a-c])", right)

    comp2 = botogram.Component("multiple")
    comp2.add_message_matches_hook(r"([a-c])_([a-c])_([a-c])", multiple,
                                    multiple=True)

    sample_update.message.text = "a_b_c c_a_b b_c_a"

    for comp in comp1, comp2:
        localbot = copy.copy(bot)
        localbot.use(comp)
        localbot.process(sample_update)

    assert wrong_processed == False
    assert right_processed == True
    assert single_processed == 1
    assert multiple_processed == 3


def test_add_command(bot, sample_update):
    sample1_processed = False
    sample2_processed = False
    sample3_processed = False

    def sample1(chat, message, args):
        nonlocal sample1_processed
        sample1_processed = True

    def sample2(chat, message, args):
        nonlocal sample2_processed
        sample2_processed = True

        assert chat.id == -1
        assert message.text == "/sample2 a b c"
        assert message.chat == chat
        assert args == ["a", "b", "c"]

    def sample3(chat, message, args):
        nonlocal sample3_processed
        sample3_processed = True

        assert message.text == "/sample3@test_bot a b c"


    comp = botogram.Component("test")
    comp.add_command("sample1", sample1)
    comp.add_command("sample2", sample2)
    comp.add_command("sample3", sample3)

    bot.use(comp)

    for cmd in "sample1@another_bot", "sample2", "sample3@test_bot":
        sample_update.message.text = "/%s a b c" % cmd
        bot.process(sample_update)

    assert sample1_processed == False
    assert sample2_processed == True
    assert sample3_processed == True


def test_add_timer(bot):
    timer1_calls = 0
    timer2_calls = 0
    timer3_calls = 0

    def timer1():
        nonlocal timer1_calls
        timer1_calls += 1

    def timer2():
        nonlocal timer2_calls
        timer2_calls += 1

    @botogram.pass_bot
    def timer3(local_bot):
        nonlocal timer3_calls
        timer3_calls += 1

        assert local_bot == bot

    comp = botogram.Component("test")
    comp.add_timer(1, timer1)
    comp.add_timer(3, timer2)
    comp.add_timer(30, timer3)

    bot.use(comp)

    # This will simulate running the bot for 10 seconds
    now = 1420070400  # 01/01/2015
    for i in range(10):
        scheduled = bot.scheduled_tasks(now+i)
        for job in scheduled:
            job()

    assert timer1_calls == 10  # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    assert timer2_calls == 4   # 0, 3, 6, 9
    assert timer3_calls == 1   # 0

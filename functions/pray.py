import random
from time import time
from settings.config import COOLDOWN
from settings.messages import messages

def pray(user_id, chat_id, message_id, bot, db):
    player = db.player_by_tgandchat(user_id, chat_id)
    level = db.level_by_id(player.player_level)
    relic_multiplier = db.relic_multiplier_by_player(player)
    income_levels = [
        0, 0.2, 0.4, 0.7, 0.9, 1, 1.4, 1.8, 2.4, 3
    ]
    income_weights = [
        1, 3, 3, 3, 5, 10, 10, 5, 5, 3
    ]
    # print(round(time()))
    if (player.last_pray + (COOLDOWN)) <= round(time()):
        income = round(random.choices(income_levels, weights=income_weights)[0] * level.income * relic_multiplier)
        player.purse += income
        text = messages['income'].format(income, player.purse)
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_to_message_id=message_id)
        player.last_pray = round(time())

    elif (player.last_pray + (COOLDOWN)) >= round(time()):
        timeout = round((player.last_pray + (COOLDOWN) - (time() ))/60)
        text = messages['timeout'].format(timeout)
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_to_message_id=message_id)

    if level.cost:
        if player.purse >= level.cost:
            player.player_level += 1
            player.purse -= level.cost
            text = messages['level_up'].format(player.player_level)
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_to_message_id=message_id)


    db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray, player.relics)


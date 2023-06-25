import random
from time import time
from settings.config import COOLDOWN

def pray(user_id, chat_id, message_id, bot, db):
    player = db.player_by_tgandchat(user_id, chat_id)
    level = db.level_by_id(player.player_level)
    income_levels = [
        0, 0.2, 0.4, 0.7, 0.9, 1, 1.4, 1.8, 2.4, 3
    ]
    income_weights = [
        1, 3, 3, 3, 5, 10, 10, 5, 5, 3
    ]
    # print(round(time()))
    if (player.last_pray + (COOLDOWN)) <= round(time()):
        income = round(random.choices(income_levels, weights=income_weights)[0] * level.income)
        player.purse += income

        message = f'''
Ты заработал *{income}* монет
Твой баланс составляет *{player.purse}* монет
'''
        bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)
        player.last_pray = round(time())

    elif (player.last_pray + (COOLDOWN)) >= round(time()):
        message = f'''
*Время еще не пришло*
Попробуй снова через *{round((player.last_pray + (COOLDOWN) - (round(time()) ))/60)}* минут
'''
        bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)

    if level.cost:
        if player.purse >= level.cost:
            player.player_level += 1
            player.purse -= level.cost
            message = f'*Ты перешел на {player.player_level} уровень*'
            bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)


    db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray)


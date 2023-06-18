from time import time
from settings.config import COOLDOWN

def me(user_id, chat_id, message_id, bot, db):
    player = db.player_by_tgandchat(user_id, chat_id)
    level = db.level_by_id(player.player_level)
    if level.cost:
        to_next_level = level.cost - player.purse
    else:
        to_next_level = "у тебя максимальный уровень"
    if (player.last_pray + (COOLDOWN)) <= round(time()):
        message = f'''
*{player.name}, вот информация о тебе:*

Твой баланс: *{player.purse}*
Твой заработок: *{level.income}*
Твои реликвии: _Скоро в игре_
Твой уровень: *{player.player_level}*
Тебе осталось до следующего уровня: *{to_next_level}*
Молитва *уже доступна*
'''

    elif (player.last_pray + (COOLDOWN)) >= round(time()):
        message = f'''
*{player.name}, вот информация о тебе:*

Твой баланс: *{player.purse}*
Твой заработок: *{level.income}*
Твои реликвии: _Скоро в игре_
Твой уровень: *{player.player_level}*
Тебе осталось до следующего уровня: *{to_next_level}*
Следующая молитва через *{round((player.last_pray + (COOLDOWN) - (round(time())))/60)}* минут
'''

    bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)
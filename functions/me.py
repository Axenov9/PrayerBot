from time import time
from settings.config import COOLDOWN

def me(user_id, chat_id, message_id, bot, db):
    player = db.player_by_tgandchat(user_id, chat_id)
    level = db.level_by_id(player.player_level)
    if level.cost:
        to_next_level = level.cost - player.purse
    else:
        to_next_level = "у тебя максимальный уровень"
    if (player.last_pray + (COOLDOWN)) <= time():
        text = f'''
*{player.name}, вот информация о тебе:*

Твой баланс: *{player.purse}*
Твой заработок: *{level.income}*
Твой бонус реликвий: *{db.relic_multiplier_by_player(player)}*
Твой уровень: *{player.player_level}*
Тебе осталось до следующего уровня: *{to_next_level}*
Твой престиж: _Скоро в игре_
Молитва *уже доступна*
'''

    elif (player.last_pray + (COOLDOWN)) >= time():
        text = f'''
*{player.name}, вот информация о тебе:*

Твой баланс: *{player.purse}*
Твой заработок: *{level.income}*
Твой бонус реликвий: *{db.relic_multiplier_by_player(player)}*
Твой уровень: *{player.player_level}*
Тебе осталось до следующего уровня: *{to_next_level}*
Твой престиж: _Скоро в игре_
Следующая молитва через *{round((player.last_pray + (COOLDOWN) - (time()))/60)}* минут
'''

    bot.send_message(chat_id, text, parse_mode='Markdown', reply_to_message_id=message_id)
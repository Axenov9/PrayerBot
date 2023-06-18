from settings.config import COOLDOWN
def op(tg_id, chat_id, message_id, user_tg_id, name, bot, db):
    if db.is_admin(tg_id):
        if not db.is_admin(user_tg_id):
            db.add_new_admin(user_tg_id, name)
            message = f'''
*{name}*, теперь вы *админ*
'''
            bot.send_message(chat_id, message, parse_mode='Markdown')
        else:
            message = f'''
Этот человек *уже админ*
            '''
            bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)
    else:
        message = f'''
У вас *нет прав* на эту команду
'''
        bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)


def skip(tg_id, chat_id, message_id, bot, db):
    if db.is_admin(tg_id):
        player = db.player_by_tgandchat(tg_id, chat_id)
        player.last_pray -= COOLDOWN
        db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray)


        message = f'''Откат на молитву *снят*'''
        bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)

    else:
        message = f'''
У вас *нет прав* на эту команду
    '''
        bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)
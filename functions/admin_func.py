from settings.config import COOLDOWN
def op(tg_id, chat_id, message_id, user_tg_id, name, bot, db):
    if db.is_admin(tg_id) and db.admin_by_tgid(tg_id).level == 0:
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


def skip(tg_id, chat_id, message_id, message, bot, db):
    if db.is_admin(tg_id):
        if message.reply_to_message:
            player = db.player_by_tgandchat(message.reply_to_message.from_user.id, chat_id)
            player.last_pray -= COOLDOWN
            db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray)
            reply_to = message.reply_to_message.message_id
            message = f'''Откат на молитву *снят*'''
            bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=reply_to)

        else:
            player = db.player_by_tgandchat(tg_id, chat_id)
            player.last_pray -= COOLDOWN
            db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray)
            reply_to = message.message_id
            message = f'''Откат на молитву *снят*'''
            bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=reply_to)




    else:
        message = f'''
У вас *нет прав* на эту команду
    '''
        bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)


def send_error(message, bot):
    text = 'Что-то *пошло не так*'
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=message.message_id)

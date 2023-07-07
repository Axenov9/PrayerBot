from settings.config import COOLDOWN, MAXLEVEL
from settings.messages import messages

def op(tg_id, chat_id, message_id, user_tg_id, name, bot, db):
    if db.is_admin(tg_id) and db.admin_by_tgid(tg_id).level == 0:
        if not db.is_admin(user_tg_id):
            db.add_new_admin(user_tg_id, name)
            message = f'*{name}*, теперь вы *админ*'
            bot.send_message(chat_id, message, parse_mode='Markdown')
        else:
            message = 'Этот человек *уже админ*'
            bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)
    else:
        message = messages['ne_rights']
        bot.send_message(chat_id, message, parse_mode='Markdown', reply_to_message_id=message_id)


def skip(tg_id, chat_id, message, bot, db):
    if db.is_admin(tg_id):
        if message.reply_to_message and db.player_by_tgandchat(message.reply_to_message.from_user.id, message.chat.id):
            player = db.player_by_tgandchat(message.reply_to_message.from_user.id, chat_id)
            player.last_pray -= COOLDOWN
            db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray, player.relics)
            reply_to = message.reply_to_message.message_id
            text = 'Откат на молитву *снят*'
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_to_message_id=reply_to)

        elif message.reply_to_message and not db.player_by_tgandchat(message.reply_to_message.from_user.id, message.chat.id):
            text = f'*{message.reply_to_message.from_user.first_name}* не является доступным игроком'
            reply_to = message.reply_to_message.message_id
            bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)

        else:
            player = db.player_by_tgandchat(tg_id, chat_id)
            player.last_pray -= COOLDOWN
            db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray, player.relics)
            reply_to = message.message_id
            text = 'Откат на молитву *снят*'
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_to_message_id=reply_to)

    else:
        text = message = messages['ne_rights']
        reply_to = message.message_id
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_to_message_id=reply_to)

def add_level(message, count, bot, db):
    if db.is_admin(message.from_user.id):
        if message.reply_to_message and db.player_by_tgandchat(message.reply_to_message.from_user.id, message.chat.id):
            player = db.player_by_tgandchat(message.reply_to_message.from_user.id, message.chat.id)
            if count.replace('-', '', 1).isdigit():
                count = int(count)
                player.player_level += count
                if player.player_level > MAXLEVEL:
                    player.player_level = MAXLEVEL
                elif player.player_level < 1:
                    player.player_level = 1
                db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray, player.relics)
                reply_to = message.reply_to_message.message_id
                if count >= 0:
                    text = f'Ваш уровень повышен на *{count}*\nВы перешли на *{player.player_level}* уровень'
                elif count <0:
                    text = f'Ваш уровень понижен на *{0 - count}*\nВы перешли на *{player.player_level}* уровень'
                bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)
            else:
                text = messages['inc_value']
                reply_to = message.message_id
                bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)

        elif message.reply_to_message and not db.player_by_tgandchat(message.reply_to_message.from_user.id, message.chat.id):
            text = f'*{message.reply_to_message.from_user.first_name}* не является доступным игроком'
            reply_to = message.reply_to_message.message_id
            bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)

        else:
            player = db.player_by_tgandchat(message.from_user.id, message.chat.id)
            if count.replace('-','',1).isdigit():
                count = int(count)
                player.player_level += count
                if player.player_level > MAXLEVEL:
                    player.player_level = MAXLEVEL
                elif player.player_level < 1:
                    player.player_level = 1
                db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray, player.relics)
                reply_to = message.message_id
                if count >= 0:
                    text = f'Ваш уровень повышен на *{count}*\nВы перешли на *{player.player_level}* уровень'
                elif count < 0:
                    text = f'Ваш уровень понижен на *{0 - count}*\nВы перешли на *{player.player_level}* уровень'
                bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)
            else:
                text = messages['inc_value']
                reply_to = message.message_id
                bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)

    else:
        text = message = messages['ne_rights']
        bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=message.message_id)


def add_purse(message, count, bot, db):
    if db.is_admin(message.from_user.id):
        if message.reply_to_message and db.player_by_tgandchat(message.reply_to_message.from_user.id, message.chat.id):
            player = db.player_by_tgandchat(message.reply_to_message.from_user.id, message.chat.id)
            if count.replace('-', '', 1).isdigit():
                count = int(count)
                player.purse += count
                if player.purse < 0:
                    player.purse = 0
                db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray, player.relics)
                reply_to = message.reply_to_message.message_id
                if count >= 0:
                    text = f'Ваш баланс повышен на *{count}*\nТеперь ваш баланс составляет {player.purse}'
                elif count <0:
                    text = f'Ваш баланс понижен на *{0 - count}*\nТеперь ваш баланс составляет {player.purse}'
                bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)
            else:
                text = messages['inc_value']
                reply_to = message.message_id
                bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)


            level = db.level_by_id(player.player_level)
            if level.cost:
                if player.purse >= level.cost:
                    while player.purse >= level.cost:
                        level = db.level_by_id(player.player_level)
                        if level.cost and player.purse >= level.cost:
                            player.player_level += 1
                            player.purse -= level.cost
                            db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray, player.relics)
                        # text = '*Ты перешел на новый уровень*'
                        # reply_to = message.message_id
                        # bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)
                        else:
                            break
                    text = messages['level_up'].format(player.player_level)
                    reply_to = message.reply_to_message.message_id
                    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)


        elif message.reply_to_message and not db.player_by_tgandchat(message.reply_to_message.from_user.id, message.chat.id):
            text = f'*{message.reply_to_message.from_user.first_name}* не является доступным игроком'
            reply_to = message.reply_to_message.message_id
            bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)

        else:
            player = db.player_by_tgandchat(message.from_user.id, message.chat.id)
            if count.replace('-','',1).isdigit():
                count = int(count)
                player.purse += count
                if player.purse < 0:
                    player.purse = 0
                db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray, player.relics)
                reply_to = message.message_id
                if count >= 0:
                    text = f'Ваш баланс повышен на *{count}*\nТеперь ваш баланс составляет {player.purse}'
                elif count < 0:
                    text = f'Ваш баланс понижен на *{0 - count}*\nТеперь ваш баланс составляет {player.purse}'
                bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)
            else:
                text = message['inc_value']
                reply_to = message.message_id
                bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)

            level = db.level_by_id(player.player_level)
            if level.cost:
                if player.purse >= level.cost:
                    while player.purse >= level.cost:
                        level = db.level_by_id(player.player_level)
                        if level.cost and player.purse >= level.cost:
                            player.player_level += 1
                            player.purse -= level.cost
                            db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray, player.relics)
                            # text = '*Ты перешел на новый уровень*'
                            # reply_to = message.message_id
                            # bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)
                        else:
                            break
                    text = messages['level_up'].format(player.player_level)
                    reply_to = message.message_id
                    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=reply_to)

    else:
        text = message = messages['ne_rights']
        bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=message.message_id)



def send_error(message, bot):
    text = messages['err']
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=message.message_id)

from settings.messages import messages
def check_player(tg_id, chat_id, db, bot,message):
    if db.player_by_tgandchat(tg_id, chat_id):
        return True
        # print(db.player_by_tgandchat(tg_id, chat_id))
    else:
        text = messages['check']
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_to_message_id=message.message_id)
        return False

        # db.add_new_player(tg_id, chat_id, message.from_user.first_name)
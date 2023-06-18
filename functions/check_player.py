def check_player(tg_id, chat_id, db, message):
    if db.player_by_tgandchat(tg_id, chat_id):
        pass
        # print(db.player_by_tgandchat(tg_id, chat_id))
    else:
        db.add_new_player(tg_id, chat_id, message.from_user.first_name)
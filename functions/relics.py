from settings.messages import messages
from models.relic import RELICS_NAME

from keyboard.relics_markup import buy_markup, buy_list_markup
def relics(message, bot, db):
    user_id = message.from_user.id
    chat_id = message.chat.id

    player = db.player_by_tgandchat(user_id, chat_id)
    relics = db.relics_by_player(player)
    print(relics)
    if relics:
        text = messages['rel_start'].format(player.name)
        multipliyer = 1
        for relic in relics:
            text = text + messages['relic_disc'].format(RELICS_NAME[relic.name], relic.multiplier) + ' '
            multipliyer += relic.multiplier
        text = text + messages['rel_end'].format(multipliyer)
    else:
        text = messages['no_relics']

    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_to_message_id=message.message_id, reply_markup=buy_markup())


def buy_relics(call, bot, db):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    player = db.player_by_tgandchat(user_id, chat_id)

    markup = buy_list_markup(player, db)
    if markup:
        text = messages['buy_relics']
        bot.edit_message_text(text, call.message.chat.id, call.message.id, parse_mode='Markdown', reply_markup=markup)
    elif not markup:
        text = messages['all_bought']
        bot.edit_message_text(text, call.message.chat.id, call.message.id, parse_mode='Markdown')


def buy_relic_by_id(call, bot, db):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    relic_id = call.data.split()[1]

    relic = db.relic_by_id(relic_id)
    player = db.player_by_tgandchat(user_id, chat_id)
    if player.purse >= relic.price:
        player.relics = player.relics + ' ' + str(relic.id)
        player.purse -= relic.price

        text = messages['bought_relic'].format(RELICS_NAME[relic.name])

    else:
        text = messages['not_enough_money']

    bot.edit_message_text(text, call.message.chat.id, call.message.id, parse_mode='Markdown')

    db.update_player_inf(player.id, player.purse, player.player_level, player.last_pray, player.relics)
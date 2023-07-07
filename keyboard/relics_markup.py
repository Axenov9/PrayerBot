from telebot.types import InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
from settings.messages import keyboard

from models.relic import RELICS_NAME
def buy_markup():
    markup = ikm()
    markup.add(ikb(keyboard['buy_relics'], parse_mode='Markdown', callback_data='buy_relics'))

    return markup

def buy_list_markup(player, db):
    markup = ikm()
    is_empty = True
    all_relics = db.all_relics()
    for relic in all_relics:
        if not str(relic.id) in player.relics and player.player_level >= relic.level_req:
            markup.add(ikb(keyboard['relic'].format(RELICS_NAME[relic.name], relic.price, relic.multiplier),
                           parse_mode='Markdown', callback_data='buy ' + str(relic.id)))
            is_empty = False

    
    if is_empty == False:
        return markup
    elif is_empty == True:
        return False
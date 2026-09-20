import logging
import os

import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException


# ============================================
# НАСТРОЙКИ
# ============================================
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN is not set. Add it to Replit Secrets before starting the bot."
    )

# Официальный сайт прописан жёстко, чтобы кнопку нельзя было перенаправить.
SITE_URL = "https://www.libertatea.ro"

# Официальный e-mail редакции (задать в переменных окружения).
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "").strip()

BRAND = "Libertatea"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# ============================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================
def btn(text, data):
    return types.InlineKeyboardButton(text=text, callback_data=data)


def site_btn():
    return types.InlineKeyboardButton(
        text=f"📰 Deschide {BRAND}",
        web_app=types.WebAppInfo(url=SITE_URL),
    )


def make_markup(rows):
    markup = types.InlineKeyboardMarkup()
    for row in rows:
        markup.row(*row)
    return markup


BTN_HEADLINES = ("📋 Titlurile zilei", "headlines")
BTN_MENU = ("🗂 Cuprins", "menu")


def article_rows():
    return [
        [site_btn()],
        [btn(*BTN_HEADLINES), btn(*BTN_MENU)],
    ]


# ============================================
# ТЕКСТЫ ЭКРАНОВ
# ============================================
TEXT_START = (
    f"📰 <b>Bun venit la {BRAND}!</b>\n\n"
    "În fiecare sezon, o mică selecție de lecturi despre cultură, "
    "bucătărie și călătorii în România, de citit liniștit direct în chat.\n\n"
    f"Pentru știrile zilei, deschideți site-ul {BRAND} cu butonul de mai jos.\n\n"
    "Pentru început, apăsați pe <b>Titlurile zilei</b>."
)

TEXT_HEADLINES = (
    "📋 <b>Titlurile zilei</b>\n\n"
    "Trei lecturi alese pentru astăzi, fiecare disponibilă integral în chat.\n\n"
    "<b>Cultură</b> — cinci muzee de vizitat în această toamnă.\n\n"
    "<b>Bucătărie</b> — cinci preparate tradiționale românești.\n\n"
    "<b>Călătorii</b> — cinci locuri de descoperit într-un weekend de toamnă.\n\n"
    "Apăsați pe un titlu pentru a deschide articolul."
)

TEXT_CULTURE = (
    "🎨 <b>Cinci muzee de vizitat în această toamnă</b>\n\n"
    "<b>București — Muzeul Național de Artă al României</b>\n"
    "Găzduit în fostul Palat Regal, reunește galerii de artă "
    "românească veche și modernă, dar și de artă europeană.\n\n"
    "<b>București — Muzeul Național al Satului „Dimitrie Gusti”</b>\n"
    "Un muzeu în aer liber, pe malul lacului Herăstrău, cu case "
    "țărănești, mori și biserici de lemn aduse din toate regiunile țării.\n\n"
    "<b>Sibiu — Muzeul Național Brukenthal</b>\n"
    "Deschis publicului în 1817, este unul dintre cele mai vechi "
    "muzee din această parte a Europei, în palatul baronului "
    "Samuel von Brukenthal.\n\n"
    "<b>Sibiu — Muzeul ASTRA</b>\n"
    "În Pădurea Dumbrava, sute de construcții tradiționale: "
    "gospodării, ateliere și instalații populare.\n\n"
    "<b>Cluj-Napoca — Muzeul de Artă</b>\n"
    "În Palatul Bánffy din Piața Unirii, o colecție bogată de "
    "pictură românească, într-una dintre cele mai elegante clădiri baroce din oraș.\n\n"
    "<i>Programul și prețurile se verifică pe site-urile oficiale ale muzeelor.</i>"
)

TEXT_CUISINE = (
    "🍲 <b>Cinci preparate tradiționale românești</b>\n\n"
    "<b>Sarmale</b>\n"
    "Foi de varză murată umplute cu carne tocată și orez, fierte "
    "încet ore în șir. Se servesc cu mămăligă și smântână.\n\n"
    "<b>Mămăligă cu brânză și smântână</b>\n"
    "Mămăligă caldă, brânză de oaie și smântână groasă. Simplă, "
    "sățioasă și iubită în toată țara.\n\n"
    "<b>Ciorbă de burtă</b>\n"
    "Ciorbă acrișoară, dreasă cu smântână și gălbenuș, servită "
    "cu usturoi, oțet și ardei iute.\n\n"
    "<b>Mici</b>\n"
    "Rulouri mici din carne tocată condimentată, fripte la grătar. "
    "Se mănâncă cu muștar și pâine proaspătă.\n\n"
    "<b>Papanași</b>\n"
    "Gogoși din brânză de vaci, servite cu smântână și dulceață "
    "de afine sau vișine.\n\n"
    "<i>Cantitățile și timpii se adaptează după gust.</i>"
)

TEXT_TRAVEL = (
    "🏡 <b>Cinci locuri pentru un weekend de toamnă</b>\n\n"
    "<b>Viscri (județul Brașov)</b>\n"
    "Sat săsesc cu o biserică fortificată inclusă în patrimoniul "
    "UNESCO. Case colorate, drumuri de țară și liniște deplină.\n\n"
    "<b>Biertan (județul Sibiu)</b>\n"
    "Una dintre cele mai impresionante biserici fortificate din "
    "Transilvania, tot în patrimoniul UNESCO.\n\n"
    "<b>Sighișoara (județul Mureș)</b>\n"
    "O cetate medievală încă locuită, cu Turnul cu Ceas, "
    "străduțe pietruite și Scara Școlarilor.\n\n"
    "<b>Săpânța (județul Maramureș)</b>\n"
    "Celebru pentru Cimitirul Vesel: cruci de lemn pictate în "
    "albastru, cu versuri pline de umor.\n\n"
    "<b>Rimetea (județul Alba)</b>\n"
    "Case albe cu ferestre verzi sub Piatra Secuiului. Se spune "
    "că aici soarele răsare de două ori, din cauza stâncii.\n\n"
    "<i>Pentru cazare, rezervarea din timp este recomandată.</i>"
)

TEXT_MENU = (
    "🗂 <b>Cuprins</b>\n\n"
    "Din acest meniu puteți:\n\n"
    "• Citi <b>titlurile zilei</b> și articolele, direct aici.\n"
    "• Consulta rubricile: Cultură, Bucătărie, Călătorii.\n"
    "• Parcurge glosarul și întrebările frecvente.\n"
    "• Afla mai multe despre publicație și cum ne puteți scrie.\n\n"
    "Pentru ediția completă, folosiți butonul de deschidere a site-ului."
)

TEXT_GLOSSARY = (
    "📖 <b>Mic glosar</b>\n\n"
    "<b>Redacție</b> — echipa care adună, selectează și pregătește "
    "textele pentru publicare.\n\n"
    "<b>Editorial</b> — articol de opinie, de obicei semnat, care "
    "exprimă poziția autorului sau a publicației.\n\n"
    "<b>Reportaj</b> — relatare jurnalistică de la fața locului, "
    "cu detalii, mărturii și atmosferă.\n\n"
    "<b>Conținut evergreen</b> — text care nu depinde de știrea "
    "zilei: cultură, călătorii, bucătărie.\n\n"
    "<b>Trimis special</b> — jurnalist care relatează direct de "
    "la locul evenimentelor.\n\n"
    "<b>Rubrică</b> — secțiune recurentă dedicată unei teme."
)

TEXT_FAQ = (
    "❓ <b>Întrebări frecvente</b>\n\n"
    "<b>Cum știu că acesta este botul oficial?</b>\n"
    f"Botul oficial {BRAND} este cel anunțat pe site-ul "
    "libertatea.ro. Butonul de deschidere duce întotdeauna la "
    "adresa www.libertatea.ro. Nu vă cerem niciodată în chat "
    "parole, coduri de confirmare sau date de card.\n\n"
    "<b>Cât de des se actualizează?</b>\n"
    "Selecția din chat se reînnoiește în fiecare sezon. Pentru "
    "știrile zilei, deschideți site-ul.\n\n"
    "<b>Cum opresc notificările?</b>\n"
    "Din setările chatului Telegram puteți dezactiva sau amuți "
    "notificările.\n\n"
    "<b>Pot distribui un articol?</b>\n"
    "Da. Folosiți funcția de redirecționare din Telegram."
)

TEXT_ABOUT = (
    f"ℹ️ <b>Despre {BRAND}</b>\n\n"
    f"{BRAND} este unul dintre cotidianele importante din România, "
    "apărut în decembrie 1989.\n\n"
    "Această versiune Telegram este gândită pentru a face mai "
    "comodă lectura conținutului evergreen direct din chat.\n\n"
    "Site-ul oficial: libertatea.ro"
)


def contact_text():
    email_line = (
        f"• E-mail: {CONTACT_EMAIL}\n"
        if CONTACT_EMAIL
        else "• Datele de contact sunt disponibile pe libertatea.ro\n"
    )
    return (
        "✏️ <b>Contact redacție</b>\n\n"
        "Pentru sugestii, corecturi sau semnalări:\n"
        + email_line
        + "\nMulțumim pentru fiecare mesaj!"
    )


# ============================================
# ЭКРАНЫ: callback_data -> (текст, кнопки)
# ============================================
SCREENS = {
    "headlines": (
        TEXT_HEADLINES,
        [
            [btn("🎨 Cultură — muzee de toamnă", "culture")],
            [btn("🍲 Bucătărie — preparate tradiționale", "cuisine")],
            [btn("🏡 Călătorii — cinci locuri", "travel")],
            [btn(*BTN_MENU)],
        ],
    ),
    "culture": (TEXT_CULTURE, article_rows()),
    "cuisine": (TEXT_CUISINE, article_rows()),
    "travel": (TEXT_TRAVEL, article_rows()),
    "menu": (
        TEXT_MENU,
        [
            [site_btn()],
            [btn(*BTN_HEADLINES)],
            [btn("📖 Glosar", "glossary"), btn("❓ Întrebări", "faq")],
            [btn("✏️ Contact", "contact"), btn(f"ℹ️ Despre {BRAND}", "about")],
        ],
    ),
    "glossary": (TEXT_GLOSSARY, [[btn(*BTN_HEADLINES)], [btn(*BTN_MENU)]]),
    "faq": (TEXT_FAQ, [[btn(*BTN_HEADLINES)], [btn(*BTN_MENU)]]),
    "contact": (
        contact_text(),
        [[btn(*BTN_MENU), btn(f"ℹ️ Despre {BRAND}", "about")]],
    ),
    "about": (
        TEXT_ABOUT,
        [[site_btn()], [btn(*BTN_MENU), btn("✏️ Contact", "contact")]],
    ),
}


# ============================================
# ОБРАБОТЧИКИ
# ============================================
@bot.message_handler(commands=["start"])
def start(message):
    markup = make_markup([[site_btn()], [btn(*BTN_HEADLINES), btn(*BTN_MENU)]])
    bot.send_message(message.chat.id, TEXT_START, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in SCREENS)
def show_screen(call):
    bot.answer_callback_query(call.id)
    text, rows = SCREENS[call.data]
    markup = make_markup(rows)
    try:
        bot.edit_message_text(
            text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup,
        )
    except ApiTelegramException:
        bot.send_message(call.message.chat.id, text, reply_markup=markup)


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    bot.set_chat_menu_button(
        menu_button=types.MenuButtonWebApp(
            type="web_app",
            text=BRAND,
            web_app=types.WebAppInfo(url=SITE_URL),
        )
    )

    logging.info("%s bot is starting", BRAND)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()

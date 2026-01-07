print("🚀 MAIN.PY STARTED")

import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# 🔐 БЕЗОПАСНЫЙ ТОКЕН
# =========================
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден. Добавь его в Railway → Variables")

bot = telebot.TeleBot(TOKEN)

# =========================
# 🧙 АРТЕФАКТЫ
# =========================
ARTIFACTS = {
    "elixir": {
        "name": "🧪 Эликсир Правды",
        "gif": "assets/elixir_truth.gif",
        "steps": [
            "🫧 {name} делает первый глоток...\nЭликсир начинает действовать. Выпей ещё",
            "✨ {name} чувствует эффект.\nИ последний глоток эликсира запей стаканом воды. Ждём, пока нальёшь. Так, всё? Запивай и жми кнопку!",
            "🔥 *ЭЛИКСИР ПРАВДЫ АКТИВИРОВАН*\n\n{name}, ты под действием эликсира.\nПожалуй, пора ответить на некоторые вопросы. Не медли, эликсир действует около двух часов. По истечению времени можешь воспользоваться им снова (не более трёх раз в день)"
        ]
    }
}

user_state = {}

# =========================
# 📜 МЕНЮ АРТЕФАКТОВ
# =========================
def artifacts_menu():
    kb = InlineKeyboardMarkup()
    for key, artifact in ARTIFACTS.items():
        kb.add(
            InlineKeyboardButton(
                artifact["name"],
                callback_data=f"menu:{key}"
            )
        )
    return kb

# =========================
# 🧪 КНОПКА
# =========================
def drink_button():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "🧪 Выпить эликсир",
            callback_data="drink"
        )
    )
    return kb

# =========================
# 🚀 START
# =========================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🧙 Добро пожаловать в Лабораторию Артефактов\n\nВыбери предмет:",
        reply_markup=artifacts_menu()
    )

# =========================
# 🧙 ВЫБОР АРТЕФАКТА
# =========================
@bot.callback_query_handler(func=lambda call: call.data.startswith("menu:"))
def choose_artifact(call):
    bot.answer_callback_query(call.id)

    key = call.data.split(":")[1]
    artifact = ARTIFACTS[key]

    user_state[call.from_user.id] = {
        "artifact": key,
        "step": 0
    }

    with open(artifact["gif"], "rb") as gif:
        bot.send_animation(
            call.message.chat.id,
            gif,
            caption="🧪 *Эликсир Правды*\n\nНажми кнопку ниже, чтобы принять.",
            reply_markup=drink_button(),
            parse_mode="Markdown"
        )

# =========================
# 🧪 ПОШАГОВОЕ ДЕЙСТВИЕ
# =========================
@bot.callback_query_handler(func=lambda call: call.data == "drink")
def drink(call):
    bot.answer_callback_query(call.id)

    uid = call.from_user.id
    name = call.from_user.first_name

    if uid not in user_state:
        return

    state = user_state[uid]
    artifact = ARTIFACTS[state["artifact"]]

    step = state["step"]
    text = artifact["steps"][step].format(name=name)
    state["step"] += 1

    if state["step"] < len(artifact["steps"]):
        markup = drink_button()
    else:
        markup = None
        user_state.pop(uid)

    bot.send_message(
        call.message.chat.id,
        text,
        reply_markup=markup,
        parse_mode="Markdown"
    )

print("🧪 BOT STARTED")
print("🤖 BOT POLLING START")
bot.infinity_polling()

bot.infinity_polling()
